// Dolg API Single Page Application Client Logic

const API_BASE = "";

// Global State
let currentUser = null;
let authToken = localStorage.getItem("dolg_token") || null;
let currentGroup = null;
let currentGroupMembers = [];

// DOM References
const authView = document.getElementById("authView");
const appView = document.getElementById("appView");
const groupsSection = document.getElementById("groupsSection");
const groupDashboard = document.getElementById("groupDashboard");

// On Load
document.addEventListener("DOMContentLoaded", () => {
  updateUILanguage();
  if (authToken) {
    fetchProfile();
  } else {
    showAuthView();
  }

  window.addEventListener("languageChanged", () => {
    if (currentGroup) {
      const activeTab = document.querySelector(".dash-tab.active");
      if (activeTab) {
        const tabName = activeTab.getAttribute("data-tab");
        loadTabContent(tabName);
      }
    }
  });
});

// Toast Notifications
function showToast(message, type = "success") {
  const container = document.getElementById("toastContainer");
  if (!container) return;
  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 4000);
}

// API Helper
async function apiRequest(endpoint, method = "GET", body = null) {
  const headers = {};
  if (authToken) {
    headers["Authorization"] = `Bearer ${authToken}`;
  }
  if (body) {
    headers["Content-Type"] = "application/json";
  }

  const options = {
    method,
    headers,
    body: body ? JSON.stringify(body) : null
  };

  const res = await fetch(`${API_BASE}${endpoint}`, options);
  if (res.status === 401) {
    logout();
    throw new Error("Unauthorized");
  }
  
  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.detail || t("errorGeneric"));
  }

  if (res.status === 204) return null;
  return await res.json();
}

// Auth Functions
function showAuthTab(tab) {
  document.getElementById("tabLoginBtn").classList.toggle("active", tab === 'login');
  document.getElementById("tabRegisterBtn").classList.toggle("active", tab === 'register');
  document.getElementById("loginForm").style.display = tab === 'login' ? 'block' : 'none';
  document.getElementById("registerForm").style.display = tab === 'register' ? 'block' : 'none';
}

async function handleLogin(e) {
  e.preventDefault();
  const email = document.getElementById("loginEmail").value;
  const password = document.getElementById("loginPassword").value;

  try {
    const data = await apiRequest("/auth/json-login", "POST", { email, password });
    authToken = data.access_token;
    localStorage.setItem("dolg_token", authToken);
    currentUser = data.user;
    showAppView();
  } catch (err) {
    showToast(err.message, "error");
  }
}

async function handleRegister(e) {
  e.preventDefault();
  const name = document.getElementById("regName").value;
  const email = document.getElementById("regEmail").value;
  const password = document.getElementById("regPassword").value;

  try {
    await apiRequest("/auth/register", "POST", { name, email, password });
    showToast(t("tabRegister") + " " + t("alertGroupCreated"));
    // Auto login
    const loginData = await apiRequest("/auth/json-login", "POST", { email, password });
    authToken = loginData.access_token;
    localStorage.setItem("dolg_token", authToken);
    currentUser = loginData.user;
    showAppView();
  } catch (err) {
    showToast(err.message, "error");
  }
}

async function fetchProfile() {
  try {
    currentUser = await apiRequest("/auth/me");
    showAppView();
  } catch (err) {
    logout();
  }
}

function logout() {
  authToken = null;
  currentUser = null;
  currentGroup = null;
  localStorage.removeItem("dolg_token");
  showAuthView();
}

function showAuthView() {
  authView.style.display = "block";
  appView.style.display = "none";
}

function showAppView() {
  authView.style.display = "none";
  appView.style.display = "block";
  
  if (currentUser) {
    document.getElementById("userAvatar").textContent = currentUser.name.charAt(0).toUpperCase();
    document.getElementById("userNameDisplay").textContent = currentUser.name;
    document.getElementById("userEmailDisplay").textContent = currentUser.email;
  }
  
  showGroupsList();
}

// Groups Management
async function showGroupsList() {
  groupsSection.style.display = "block";
  groupDashboard.style.display = "none";
  currentGroup = null;

  try {
    const groups = await apiRequest("/groups");
    renderGroupsGrid(groups);
  } catch (err) {
    showToast(err.message, "error");
  }
}

function renderGroupsGrid(groups) {
  const grid = document.getElementById("groupsGrid");
  grid.innerHTML = "";

  if (groups.length === 0) {
    grid.innerHTML = `<div class="glass-card" style="grid-column: 1/-1; text-align:center; color: var(--text-muted);">${t("noGroupsYet")}</div>`;
    return;
  }

  groups.forEach(g => {
    const card = document.createElement("div");
    card.className = "glass-card group-card";
    card.onclick = () => openGroup(g.id);
    card.innerHTML = `
      <div class="group-card-header">
        <div class="group-title">${escapeHtml(g.name)}</div>
      </div>
      <div class="group-desc">${escapeHtml(g.description || "")}</div>
      <div class="group-footer">
        <span>ID #${g.id}</span>
        <span>${new Date(g.created_at).toLocaleDateString()}</span>
      </div>
    `;
    grid.appendChild(card);
  });
}

function openCreateGroupModal() {
  document.getElementById("createGroupModal").classList.add("active");
}

function closeCreateGroupModal() {
  document.getElementById("createGroupModal").classList.remove("active");
}

async function handleCreateGroup(e) {
  e.preventDefault();
  const name = document.getElementById("groupNameInput").value;
  const description = document.getElementById("groupDescInput").value;

  try {
    const group = await apiRequest("/groups", "POST", { name, description });
    closeCreateGroupModal();
    showToast(t("alertGroupCreated"));
    openGroup(group.id);
  } catch (err) {
    showToast(err.message, "error");
  }
}

// Group Dashboard
async function openGroup(groupId) {
  try {
    currentGroup = await apiRequest(`/groups/${groupId}`);
    currentGroupMembers = currentGroup.members.map(m => m.user);

    groupsSection.style.display = "none";
    groupDashboard.style.display = "block";

    document.getElementById("dashGroupName").textContent = currentGroup.name;
    document.getElementById("dashGroupDesc").textContent = currentGroup.description || "";
    
    // Member list pill
    const memberNames = currentGroup.members.map(m => m.user.name).join(", ");
    document.getElementById("dashGroupMembers").textContent = `${currentGroup.members.length} ${t("groupMembers")}: ${memberNames}`;

    switchDashTab("expenses");
  } catch (err) {
    showToast(err.message, "error");
  }
}

function switchDashTab(tabName) {
  document.querySelectorAll(".dash-tab").forEach(btn => {
    btn.classList.toggle("active", btn.getAttribute("data-tab") === tabName);
  });

  loadTabContent(tabName);
}

function loadTabContent(tabName) {
  const container = document.getElementById("dashTabContent");
  container.innerHTML = "";

  if (tabName === "expenses") {
    renderExpensesTab(container);
  } else if (tabName === "balance") {
    renderBalanceTab(container);
  } else if (tabName === "analytics") {
    renderAnalyticsTab(container);
  }
}

// 1. EXPENSES TAB
async function renderExpensesTab(container) {
  container.innerHTML = `
    <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 1.5rem;">
      <div class="glass-card">
        <h3 style="margin-bottom: 1rem;">${t("titleAddExpense")}</h3>
        <form onsubmit="handleAddExpense(event)">
          <div class="form-group">
            <label>${t("labelExpenseDesc")}</label>
            <input type="text" id="expDesc" class="form-control" required placeholder="${t("phExpenseDesc")}">
          </div>
          <div class="form-group">
            <label>${t("labelExpenseAmount")}</label>
            <input type="number" step="0.01" id="expAmount" class="form-control" required placeholder="0.00">
          </div>
          <div class="form-group">
            <label>${t("labelExpenseCategory")}</label>
            <select id="expCategory" class="form-control">
              <option value="Food & Drinks">Food & Drinks / Еда и напитки</option>
              <option value="Transportation">Transportation / Транспорт</option>
              <option value="Accommodation">Accommodation / Жилье</option>
              <option value="Entertainment">Entertainment / Развлечения</option>
              <option value="General">General / Общие</option>
            </select>
          </div>
          <div class="form-group">
            <label>${t("labelSplitType")}</label>
            <select id="expSplitType" class="form-control">
              <option value="equal">${t("splitEqual")}</option>
            </select>
          </div>
          <button type="submit" class="btn btn-primary" style="width: 100%;">${t("btnSubmitExpense")}</button>
        </form>
      </div>

      <div class="glass-card">
        <h3 style="margin-bottom: 1rem;">${t("titleExpensesHistory")}</h3>
        <div id="expensesList">Loading...</div>
      </div>
    </div>
  `;

  loadExpensesList();
}

async function loadExpensesList() {
  const listEl = document.getElementById("expensesList");
  try {
    const expenses = await apiRequest(`/groups/${currentGroup.id}/expenses`);
    if (expenses.length === 0) {
      listEl.innerHTML = `<p style="color: var(--text-muted);">${t("noExpensesYet")}</p>`;
      return;
    }

    listEl.innerHTML = expenses.map(exp => `
      <div style="padding: 1rem; background: rgba(15,23,42,0.6); border: 1px solid var(--border-color); border-radius: var(--radius-md); margin-bottom: 0.75rem; display: flex; justify-content: space-between; align-items: center;">
        <div>
          <div style="font-weight: 700; font-size: 1.1rem;">${escapeHtml(exp.description)}</div>
          <div style="font-size: 0.85rem; color: var(--text-muted);">
            <span style="color: var(--primary); font-weight: 600;">${escapeHtml(exp.payer.name)}</span> ${t("paidBy")} <strong>${exp.amount.toFixed(2)}</strong> | ${exp.category}
          </div>
        </div>
        <div style="text-align: right;">
          <div style="font-weight: 800; font-size: 1.2rem; color: var(--secondary);">${exp.amount.toFixed(2)}</div>
          ${exp.paid_by === currentUser.id ? `<button class="btn btn-danger btn-sm" onclick="deleteExpense(${exp.id})">${t("deleteExpense")}</button>` : ""}
        </div>
      </div>
    `).join("");
  } catch (err) {
    listEl.innerHTML = `<p style="color: var(--danger);">${err.message}</p>`;
  }
}

async function handleAddExpense(e) {
  e.preventDefault();
  const description = document.getElementById("expDesc").value;
  const amount = parseFloat(document.getElementById("expAmount").value);
  const category = document.getElementById("expCategory").value;
  const split_type = document.getElementById("expSplitType").value;

  try {
    await apiRequest(`/groups/${currentGroup.id}/expenses`, "POST", {
      description,
      amount,
      category,
      split_type
    });
    showToast(t("alertExpenseAdded"));
    loadExpensesList();
    document.getElementById("expDesc").value = "";
    document.getElementById("expAmount").value = "";
  } catch (err) {
    showToast(err.message, "error");
  }
}

async function deleteExpense(expId) {
  if (!confirm("Are you sure you want to delete this expense?")) return;
  try {
    await apiRequest(`/groups/${currentGroup.id}/expenses/${expId}`, "DELETE");
    showToast(t("alertExpenseDeleted"));
    loadExpensesList();
  } catch (err) {
    showToast(err.message, "error");
  }
}

// 2. BALANCE & SETTLE UP TAB
async function renderBalanceTab(container) {
  container.innerHTML = `
    <div style="display: flex; flex-direction: column; gap: 1.5rem;">
      <div class="glass-card">
        <h3>${t("titleGroupBalance")}</h3>
        <div id="balanceTableContainer">Loading...</div>
      </div>

      <div class="glass-card">
        <h3>${t("titleSettleUpPlan")}</h3>
        <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 1rem;">${t("settleUpSubtitle")}</p>
        <div id="settleUpContainer">Loading...</div>
      </div>
    </div>
  `;

  loadBalanceData();
}

async function loadBalanceData() {
  const tableEl = document.getElementById("balanceTableContainer");
  const settleEl = document.getElementById("settleUpContainer");

  try {
    const balances = await apiRequest(`/groups/${currentGroup.id}/balance`);
    const transactions = await apiRequest(`/groups/${currentGroup.id}/settle-up`);

    // Render Balances Table
    let tableHtml = `
      <div class="table-responsive">
        <table class="custom-table">
          <thead>
            <tr>
              <th>${t("colMember")}</th>
              <th>${t("colPaid")}</th>
              <th>${t("colOwed")}</th>
              <th>${t("colSettledNet")}</th>
              <th>${t("colNetBalance")}</th>
            </tr>
          </thead>
          <tbody>
    `;

    balances.members.forEach(m => {
      let netClass = "badge-net-zero";
      let statusLabel = t("statusSettled");
      if (m.net_balance > 0.005) {
        netClass = "badge-net-pos";
        statusLabel = `+${m.net_balance.toFixed(2)} (${t("statusOwedToYou")})`;
      } else if (m.net_balance < -0.005) {
        netClass = "badge-net-neg";
        statusLabel = `${m.net_balance.toFixed(2)} (${t("statusYouOwe")})`;
      }

      tableHtml += `
        <tr>
          <td><strong>${escapeHtml(m.user_name)}</strong></td>
          <td>${m.paid_total.toFixed(2)}</td>
          <td>${m.owed_total.toFixed(2)}</td>
          <td>${(m.settlements_paid - m.settlements_received).toFixed(2)}</td>
          <td class="${netClass}">${statusLabel}</td>
        </tr>
      `;
    });

    tableHtml += `</tbody></table></div>`;
    tableEl.innerHTML = tableHtml;

    // Render Settle Up Transactions
    if (transactions.length === 0) {
      settleEl.innerHTML = `<p style="color: var(--secondary); font-size: 1.1rem; font-weight: 600;">${t("noDebtsAllSettled")}</p>`;
      return;
    }

    let settleHtml = "";
    transactions.forEach(tItem => {
      const isMyDebt = tItem.from_user_id === currentUser.id;
      settleHtml += `
        <div class="settlement-card">
          <div class="settlement-info">
            <span style="font-weight: 700;">${escapeHtml(tItem.from_user_name)}</span>
            <span style="color: var(--text-muted);">${t("payerPaysPayee")}</span>
            <span style="font-weight: 700; color: var(--primary);">${escapeHtml(tItem.to_user_name)}</span>
          </div>
          <div style="display: flex; align-items: center; gap: 1rem;">
            <div class="settlement-amount">${tItem.amount.toFixed(2)}</div>
            ${isMyDebt ? `<button class="btn btn-success btn-sm" onclick="recordPayOff(${tItem.to_user_id}, ${tItem.amount})">${t("btnRecordPay")}</button>` : ""}
          </div>
        </div>
      `;
    });

    settleEl.innerHTML = settleHtml;
  } catch (err) {
    tableEl.innerHTML = `<p style="color: var(--danger);">${err.message}</p>`;
  }
}

async function recordPayOff(payeeId, amount) {
  try {
    await apiRequest(`/groups/${currentGroup.id}/settlements`, "POST", {
      payee_id: payeeId,
      amount: amount
    });
    showToast(t("alertSettlementRecorded"));
    loadBalanceData();
  } catch (err) {
    showToast(err.message, "error");
  }
}

// 3. ANALYTICS TAB
async function renderAnalyticsTab(container) {
  container.innerHTML = `
    <div class="glass-card">
      <h3 style="margin-bottom: 1.5rem;">${t("titleAnalytics")}</h3>
      <div id="analyticsContent">Loading Data Science Metrics...</div>
    </div>
  `;

  loadAnalytics();
}

async function loadAnalytics() {
  const contentEl = document.getElementById("analyticsContent");
  try {
    const analytics = await apiRequest(`/groups/${currentGroup.id}/analytics`);

    contentEl.innerHTML = `
      <div class="stat-grid">
        <div class="stat-card">
          <div class="stat-label">${t("cardTotalSpent")}</div>
          <div class="stat-value">${analytics.total_spent_amount.toFixed(2)}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">${t("cardAvgExpense")}</div>
          <div class="stat-value">${analytics.average_expense_amount.toFixed(2)}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">${t("cardTopCategory")}</div>
          <div class="stat-value" style="font-size: 1.2rem;">${analytics.highest_spending_category || "N/A"}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">${t("cardExpenseCount")}</div>
          <div class="stat-value">${analytics.total_expenses_count}</div>
        </div>
      </div>

      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-top: 1.5rem;">
        <div>
          <h4>${t("titleCategoryBreakdown")}</h4>
          <table class="custom-table">
            <thead>
              <tr>
                <th>Category</th>
                <th>Amount</th>
                <th>Share</th>
              </tr>
            </thead>
            <tbody>
              ${analytics.categories.map(c => `
                <tr>
                  <td>${escapeHtml(c.category)}</td>
                  <td>${c.total_amount.toFixed(2)}</td>
                  <td><strong>${c.percentage.toFixed(1)}%</strong></td>
                </tr>
              `).join("")}
            </tbody>
          </table>
        </div>

        <div>
          <h4>${t("titleTopSpenders")}</h4>
          <table class="custom-table">
            <thead>
              <tr>
                <th>User</th>
                <th>Total Spent</th>
              </tr>
            </thead>
            <tbody>
              ${analytics.top_spenders.map(s => `
                <tr>
                  <td>${escapeHtml(s.user_name)}</td>
                  <td><strong>${s.total_spent.toFixed(2)}</strong></td>
                </tr>
              `).join("")}
            </tbody>
          </table>
        </div>
      </div>
    `;
  } catch (err) {
    contentEl.innerHTML = `<p style="color: var(--danger);">${err.message}</p>`;
  }
}

// Add Member Modal
function openAddMemberModal() {
  document.getElementById("addMemberModal").classList.add("active");
}
function closeAddMemberModal() {
  document.getElementById("addMemberModal").classList.remove("active");
}

async function handleAddMember(e) {
  e.preventDefault();
  const email = document.getElementById("memberEmailInput").value;
  try {
    await apiRequest(`/groups/${currentGroup.id}/members`, "POST", { email });
    closeAddMemberModal();
    showToast(t("alertMemberAdded"));
    openGroup(currentGroup.id);
  } catch (err) {
    showToast(err.message, "error");
  }
}

// Utility
function escapeHtml(str) {
  if (!str) return "";
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
