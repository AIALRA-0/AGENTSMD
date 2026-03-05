const treeRoot = document.getElementById("tree-root");
const recentRoot = document.getElementById("recent-root");
const editor = document.getElementById("editor");
const preview = document.getElementById("preview");
const statusEl = document.getElementById("status");
const outputEl = document.getElementById("output");
const currentFileEl = document.getElementById("current-file");
const lastCommandEl = document.getElementById("last-command");
const themeBtn = document.getElementById("btn-theme");
const sortSelect = document.getElementById("file-sort");

const EXPANDED_KEY = "agentsmd.tree.expanded.v1";
const THEME_KEY = "agentsmd.theme.v1";
const SORT_KEY = "agentsmd.file.sort.v1";
const SORT_VALUES = new Set(["name_asc", "name_desc", "mtime_desc", "mtime_asc"]);

let currentFile = "";
let latestTree = null;
let expandedMap = loadExpandedMap();
let currentTheme = "light";
let currentSort = loadSortPreference();

function loadExpandedMap() {
  try {
    const raw = localStorage.getItem(EXPANDED_KEY);
    if (!raw) return {};
    const parsed = JSON.parse(raw);
    return parsed && typeof parsed === "object" ? parsed : {};
  } catch {
    return {};
  }
}

function saveExpandedMap() {
  localStorage.setItem(EXPANDED_KEY, JSON.stringify(expandedMap));
}

function detectSystemTheme() {
  try {
    if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
      return "dark";
    }
  } catch {
    return "light";
  }
  return "light";
}

function loadTheme() {
  try {
    const saved = localStorage.getItem(THEME_KEY);
    if (saved === "light" || saved === "dark") return saved;
  } catch {
    return detectSystemTheme();
  }
  return detectSystemTheme();
}

function loadSortPreference() {
  try {
    const saved = localStorage.getItem(SORT_KEY);
    if (saved && SORT_VALUES.has(saved)) return saved;
  } catch {
    return "name_asc";
  }
  return "name_asc";
}

function saveSortPreference(mode) {
  try {
    localStorage.setItem(SORT_KEY, mode);
  } catch {
    // ignore storage write failure
  }
}

function updateThemeButton() {
  if (!themeBtn) return;
  themeBtn.textContent = currentTheme === "dark" ? "切换日间" : "切换夜间";
}

function applyTheme(theme) {
  currentTheme = theme === "dark" ? "dark" : "light";
  document.documentElement.setAttribute("data-theme", currentTheme);
  try {
    localStorage.setItem(THEME_KEY, currentTheme);
  } catch {
    // ignore storage write failure
  }
  updateThemeButton();
}

function toggleTheme() {
  applyTheme(currentTheme === "dark" ? "light" : "dark");
}

function setStatus(text, kind = "info") {
  statusEl.textContent = text;
  statusEl.style.color = kind === "error" ? "#b91c1c" : kind === "ok" ? "#15803d" : "#5f6f8d";
}

function setOutput(command, stdout, stderr) {
  lastCommandEl.textContent = command || "-";
  const parts = [];
  if (stdout) parts.push(stdout);
  if (stderr) parts.push(`\n[stderr]\n${stderr}`);
  outputEl.textContent = parts.join("\n").trim() || "(无输出)";
}

function inferScope(path) {
  if (!path || !path.includes("/")) return null;
  return path.split("/")[0] || null;
}

async function fetchJson(url, options = {}) {
  const resp = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!resp.ok) {
    const txt = await resp.text();
    throw new Error(txt || `HTTP ${resp.status}`);
  }
  return resp.json();
}

function setDirExpanded(path, expanded) {
  if (!path || path === ".") return;
  expandedMap[path] = !!expanded;
  saveExpandedMap();
}

function getDirExpanded(path) {
  return !!expandedMap[path];
}

function collectDirPaths(node, out = []) {
  if (!node) return out;
  if (node.type === "dir" && node.path !== ".") out.push(node.path);
  for (const child of node.children || []) {
    collectDirPaths(child, out);
  }
  return out;
}

function sortByName(a, b) {
  return (a.name || "").localeCompare(b.name || "", "zh-CN", { sensitivity: "base" });
}

function sortFiles(files) {
  const list = [...files];
  if (currentSort === "name_desc") {
    list.sort((a, b) => sortByName(b, a));
    return list;
  }
  if (currentSort === "mtime_desc") {
    list.sort((a, b) => {
      const ta = Number(a.modified_ts || 0);
      const tb = Number(b.modified_ts || 0);
      if (tb !== ta) return tb - ta;
      return sortByName(a, b);
    });
    return list;
  }
  if (currentSort === "mtime_asc") {
    list.sort((a, b) => {
      const ta = Number(a.modified_ts || 0);
      const tb = Number(b.modified_ts || 0);
      if (ta !== tb) return ta - tb;
      return sortByName(a, b);
    });
    return list;
  }
  list.sort(sortByName);
  return list;
}

function flattenFiles(node, out = []) {
  if (!node) return out;
  if (node.type === "file") out.push(node);
  for (const child of node.children || []) {
    flattenFiles(child, out);
  }
  return out;
}

function formatModifiedAt(node) {
  const text = node?.modified_at || "";
  return text ? text.replace(" UTC", "") : "-";
}

function ensureAncestorsExpanded(path) {
  if (!path) return;
  const parts = path.split("/");
  if (parts.length <= 1) return;
  for (let i = 1; i < parts.length; i += 1) {
    const p = parts.slice(0, i).join("/");
    expandedMap[p] = true;
  }
  saveExpandedMap();
}

function renderNode(node, container, depth = 0) {
  const li = document.createElement("li");
  li.className = "tree-node";
  li.style.setProperty("--depth", String(depth));

  if (node.type === "dir") {
    const row = document.createElement("div");
    row.className = "tree-row tree-dir";

    const toggle = document.createElement("button");
    toggle.className = "tree-toggle";
    toggle.type = "button";

    const name = document.createElement("span");
    name.className = "tree-name";
    name.textContent = node.name;

    const childrenList = document.createElement("ul");
    childrenList.className = "tree-children";

    const expanded = getDirExpanded(node.path);
    toggle.textContent = expanded ? "▾" : "▸";
    childrenList.hidden = !expanded;

    const onToggle = () => {
      const next = childrenList.hidden;
      childrenList.hidden = !next;
      toggle.textContent = next ? "▾" : "▸";
      setDirExpanded(node.path, next);
    };

    toggle.onclick = onToggle;
    name.onclick = onToggle;

    row.appendChild(toggle);
    row.appendChild(document.createTextNode("📁"));
    row.appendChild(name);
    li.appendChild(row);

    const allChildren = node.children || [];
    const dirChildren = [...allChildren.filter((c) => c.type === "dir")].sort(sortByName);
    const fileChildren = sortFiles(allChildren.filter((c) => c.type === "file"));
    for (const child of [...dirChildren, ...fileChildren]) {
      renderNode(child, childrenList, depth + 1);
    }
    li.appendChild(childrenList);
  } else {
    const row = document.createElement("div");
    row.className = "tree-row tree-file";
    row.dataset.path = node.path;

    const spacer = document.createElement("span");
    spacer.className = "tree-spacer";
    spacer.textContent = " ";

    const name = document.createElement("span");
    name.className = "tree-name";
    name.textContent = node.name;

    row.appendChild(spacer);
    row.appendChild(document.createTextNode("📄"));
    row.appendChild(name);

    row.onclick = () => openFile(node.path, row);
    li.appendChild(row);
  }

  container.appendChild(li);
}

function markActiveFile() {
  document.querySelectorAll(".tree-file.active").forEach((el) => el.classList.remove("active"));
  document.querySelectorAll(".recent-item.active").forEach((el) => el.classList.remove("active"));
  if (!currentFile) return;
  const current = document.querySelector(`.tree-file[data-path="${CSS.escape(currentFile)}"]`);
  if (current) current.classList.add("active");
  const recent = document.querySelector(`.recent-item[data-path="${CSS.escape(currentFile)}"]`);
  if (recent) recent.classList.add("active");
}

function renderRecentFiles(tree) {
  if (!recentRoot) return;
  recentRoot.innerHTML = "";
  const files = flattenFiles(tree, []);
  files.sort((a, b) => {
    const ta = Number(a.modified_ts || 0);
    const tb = Number(b.modified_ts || 0);
    if (tb !== ta) return tb - ta;
    return sortByName(a, b);
  });

  const top = files.slice(0, 12);
  if (top.length === 0) {
    const empty = document.createElement("li");
    empty.className = "recent-item";
    empty.textContent = "暂无文件";
    recentRoot.appendChild(empty);
    return;
  }

  for (const file of top) {
    const li = document.createElement("li");
    li.className = "recent-item";
    li.dataset.path = file.path;

    const name = document.createElement("span");
    name.className = "recent-name";
    name.textContent = file.path;

    const time = document.createElement("span");
    time.className = "recent-time";
    time.textContent = formatModifiedAt(file);

    li.appendChild(name);
    li.appendChild(time);
    li.onclick = () => openFile(file.path);
    recentRoot.appendChild(li);
  }
}

function renderTree(tree) {
  treeRoot.innerHTML = "";
  const list = document.createElement("ul");
  list.className = "tree-list";
  for (const child of tree.children || []) {
    renderNode(child, list, 0);
  }
  treeRoot.appendChild(list);
  renderRecentFiles(tree);
  markActiveFile();
}

async function loadTree() {
  setStatus("加载文件树...");
  try {
    const tree = await fetchJson("/api/tree");
    latestTree = tree;
    if (sortSelect) sortSelect.value = currentSort;
    renderTree(tree);
    setStatus("文件树已更新", "ok");
  } catch (err) {
    setStatus(`文件树加载失败: ${err.message}`, "error");
  }
}

async function openFile(path, targetEl) {
  try {
    const data = await fetchJson(`/api/file?path=${encodeURIComponent(path)}`);
    currentFile = path;
    ensureAncestorsExpanded(path);
    editor.value = data.content;
    currentFileEl.textContent = path;
    if (targetEl) {
      document.querySelectorAll(".tree-file.active").forEach((el) => el.classList.remove("active"));
      targetEl.classList.add("active");
    } else {
      markActiveFile();
    }
    await renderPreview();
    setStatus(`已打开: ${path}`, "ok");
  } catch (err) {
    setStatus(`打开失败: ${err.message}`, "error");
  }
}

async function renderPreview() {
  try {
    const data = await fetchJson("/api/render", {
      method: "POST",
      body: JSON.stringify({ content: editor.value }),
    });
    preview.innerHTML = data.html;
    setStatus("预览已更新", "ok");
  } catch (err) {
    setStatus(`渲染失败: ${err.message}`, "error");
  }
}

async function saveFile() {
  if (!currentFile) {
    setStatus("请先选择文件", "error");
    return;
  }

  try {
    let resp = await fetchJson("/api/file/save", {
      method: "POST",
      body: JSON.stringify({ path: currentFile, content: editor.value, confirm_protected: false }),
    });

    if (!resp.saved && resp.requires_confirmation) {
      const msg = `该文件受保护，是否确认保存？\n\n命中规则:\n${(resp.matched_rules || []).join("\n")}`;
      const ok = window.confirm(msg);
      if (!ok) {
        setStatus("已取消受保护文件保存", "info");
        return;
      }
      resp = await fetchJson("/api/file/save", {
        method: "POST",
        body: JSON.stringify({ path: currentFile, content: editor.value, confirm_protected: true }),
      });
    }

    setStatus(`保存成功: ${currentFile} (${resp.bytes || 0} bytes)`, "ok");
  } catch (err) {
    setStatus(`保存失败: ${err.message}`, "error");
  }
}

async function runAction(endpoint, scopeAware = false) {
  try {
    const payload = { scope: scopeAware ? inferScope(currentFile) : null };
    const data = await fetchJson(endpoint, {
      method: "POST",
      body: JSON.stringify(payload),
    });
    setOutput(data.command, data.stdout, data.stderr);
    if (data.ok) {
      setStatus("执行成功", "ok");
      if (endpoint.includes("index-sync") || endpoint.includes("md-sync")) {
        await loadTree();
      }
    } else {
      setStatus(`执行失败: ${data.returncode}`, "error");
    }
  } catch (err) {
    setStatus(`执行失败: ${err.message}`, "error");
  }
}

async function manualBackup() {
  try {
    const data = await fetchJson("/api/backup/manual", { method: "POST", body: JSON.stringify({}) });
    setOutput("manual-backup", `备份完成\n${data.backup_path}\n${data.size_bytes} bytes`, "");
    setStatus("备份完成", "ok");
  } catch (err) {
    setStatus(`备份失败: ${err.message}`, "error");
  }
}

function expandAll() {
  if (!latestTree) return;
  for (const path of collectDirPaths(latestTree)) {
    expandedMap[path] = true;
  }
  saveExpandedMap();
  renderTree(latestTree);
}

function collapseAll() {
  expandedMap = {};
  saveExpandedMap();
  if (latestTree) renderTree(latestTree);
}

function onSortChange() {
  if (!sortSelect) return;
  const mode = sortSelect.value;
  if (!SORT_VALUES.has(mode)) return;
  currentSort = mode;
  saveSortPreference(mode);
  if (latestTree) renderTree(latestTree);
}

document.getElementById("btn-refresh-tree").onclick = loadTree;
document.getElementById("btn-render").onclick = renderPreview;
document.getElementById("btn-save").onclick = saveFile;
document.getElementById("btn-lint").onclick = () => runAction("/api/actions/lint", false);
document.getElementById("btn-index-sync").onclick = () => runAction("/api/actions/index-sync", true);
document.getElementById("btn-md-sync").onclick = () => runAction("/api/actions/md-sync", true);
document.getElementById("btn-backup").onclick = manualBackup;
document.getElementById("btn-tree-expand-all").onclick = expandAll;
document.getElementById("btn-tree-collapse-all").onclick = collapseAll;
if (themeBtn) themeBtn.onclick = toggleTheme;
if (sortSelect) sortSelect.onchange = onSortChange;

applyTheme(loadTheme());
loadTree();
