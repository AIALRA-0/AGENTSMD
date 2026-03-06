const test = require("node:test");
const assert = require("node:assert/strict");
const http = require("node:http");
const { setTimeout: delay } = require("node:timers/promises");

function createScenarioServer(scenario) {
  let index = 0;
  const server = http.createServer(async (req, res) => {
    if (req.url !== "/api/config/validate") {
      res.statusCode = 404;
      res.end("not found");
      return;
    }

    const step = scenario[Math.min(index, scenario.length - 1)];
    index += 1;

    if (step.type === "timeout") {
      await delay(step.delayMs ?? 200);
      if (!res.writableEnded) {
        res.destroy();
      }
      return;
    }

    if (step.type === "status") {
      res.statusCode = step.code;
      res.setHeader("content-type", "application/json");
      res.end(JSON.stringify({ ok: step.code < 400, code: step.code }));
      return;
    }

    res.statusCode = 500;
    res.end("invalid scenario");
  });

  return server;
}

async function startServer(server) {
  await new Promise((resolve, reject) => {
    server.once("error", reject);
    server.listen(0, "127.0.0.1", resolve);
  });
  const addr = server.address();
  return `http://127.0.0.1:${addr.port}`;
}

async function stopServer(server) {
  await new Promise((resolve) => server.close(resolve));
}

async function validateWithRetry(url, opts = {}) {
  const timeoutMs = opts.timeoutMs ?? 80;
  const maxAttempts = opts.maxAttempts ?? 3;
  let attempts = 0;

  while (attempts < maxAttempts) {
    attempts += 1;
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);
    try {
      const res = await fetch(`${url}/api/config/validate`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ scope: "provider" }),
        signal: controller.signal,
      });
      clearTimeout(timer);

      if (res.ok) {
        return { ok: true, attempts, status: res.status };
      }
      if (res.status === 429 || res.status >= 500) {
        if (attempts < maxAttempts) {
          await delay(10);
          continue;
        }
      }
      return { ok: false, attempts, status: res.status };
    } catch (err) {
      clearTimeout(timer);
      const retryable = err && err.name === "AbortError";
      if (retryable && attempts < maxAttempts) {
        await delay(10);
        continue;
      }
      return { ok: false, attempts, error: String(err) };
    }
  }

  return { ok: false, attempts, error: "exhausted" };
}

test("configValidationFlow retries timeout then succeeds", async (t) => {
  const server = createScenarioServer([
    { type: "timeout", delayMs: 200 },
    { type: "status", code: 200 },
  ]);

  let baseUrl;
  try {
    baseUrl = await startServer(server);
  } catch (err) {
    if (err && err.code === "EPERM") {
      t.skip("current environment disallows local port listen (EPERM)");
      return;
    }
    throw err;
  }

  try {
    const result = await validateWithRetry(baseUrl, { timeoutMs: 60, maxAttempts: 3 });
    assert.equal(result.ok, true);
    assert.equal(result.attempts, 2);
  } finally {
    await stopServer(server);
  }
});

test("configValidationFlow retries on HTTP 429", async (t) => {
  const server = createScenarioServer([
    { type: "status", code: 429 },
    { type: "status", code: 200 },
  ]);

  let baseUrl;
  try {
    baseUrl = await startServer(server);
  } catch (err) {
    if (err && err.code === "EPERM") {
      t.skip("current environment disallows local port listen (EPERM)");
      return;
    }
    throw err;
  }

  try {
    const result = await validateWithRetry(baseUrl, { maxAttempts: 3 });
    assert.equal(result.ok, true);
    assert.equal(result.attempts, 2);
  } finally {
    await stopServer(server);
  }
});

test("configValidationFlow retries on HTTP 5xx then succeeds", async (t) => {
  const server = createScenarioServer([
    { type: "status", code: 503 },
    { type: "status", code: 502 },
    { type: "status", code: 200 },
  ]);

  let baseUrl;
  try {
    baseUrl = await startServer(server);
  } catch (err) {
    if (err && err.code === "EPERM") {
      t.skip("current environment disallows local port listen (EPERM)");
      return;
    }
    throw err;
  }

  try {
    const result = await validateWithRetry(baseUrl, { maxAttempts: 3 });
    assert.equal(result.ok, true);
    assert.equal(result.attempts, 3);
  } finally {
    await stopServer(server);
  }
});
