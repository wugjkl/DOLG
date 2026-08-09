const translations = {
  en: {
    appName: "Dolg API",
    tagline: "Smart Group Expense & Debt Minimization Engine",
    langButton: "🇷🇺 РУС",
    navDocs: "Swagger API Docs",
    navGithub: "GitHub Repo",
    authTitle: "Welcome to Dolg",
    authSubtitle: "Sign in or register to manage group expenses effortlessly",
    tabLogin: "Login",
    tabRegister: "Register",
    labelEmail: "Email Address",
    labelPassword: "Password",
    labelName: "Full Name",
    btnLogin: "Sign In",
    btnRegister: "Create Account",
    lblLoggedInAs: "Logged in as",
    btnLogout: "Sign Out",
    
    // Groups Section
    titleGroups: "Your Groups",
    btnCreateGroup: "+ Create New Group",
    groupMembers: "members",
    groupOwner: "Owner",
    noGroupsYet: "You don't belong to any groups yet. Create one to get started!",
    
    // Create Group Modal/Form
    modalCreateGroupTitle: "Create Expense Group",
    labelGroupName: "Group Name",
    labelGroupDesc: "Description (Optional)",
    phGroupName: "e.g., Summer Trip to Almaty",
    phGroupDesc: "e.g., Joint trip expenses and food",
    btnSubmitGroup: "Create Group",
    btnCancel: "Cancel",
    
    // Group Dashboard View
    btnBackGroups: "← Back to Groups",
    tabExpenses: "Expenses",
    tabBalance: "Balances & Settle Up",
    tabAnalytics: "Analytics",
    
    // Add Member
    btnAddMember: "+ Add Member",
    phMemberEmail: "Member's email address",
    btnSubmitMember: "Add to Group",

    // Expenses Tab
    titleAddExpense: "Add New Expense",
    labelExpenseDesc: "Description",
    phExpenseDesc: "e.g., Dinner at Restaurant",
    labelExpenseAmount: "Amount (₸ / $)",
    labelExpenseCategory: "Category",
    labelSplitType: "Split Strategy",
    splitEqual: "Equal Split",
    splitExact: "Exact Amount Split",
    btnSubmitExpense: "Add Expense",
    titleExpensesHistory: "Expense History",
    noExpensesYet: "No expenses recorded yet in this group.",
    paidBy: "paid by",
    splitEquallyAmong: "split equally among",
    deleteExpense: "Delete",

    // Balance Tab
    titleGroupBalance: "Net Balance Overview",
    colMember: "Member",
    colPaid: "Paid Total",
    colOwed: "Owed Total",
    colSettledNet: "Settlement Paid/Recv",
    colNetBalance: "Net Balance",
    statusOwedToYou: "Owed to you",
    statusYouOwe: "You owe",
    statusSettled: "Settled up",
    
    titleSettleUpPlan: "Greedy Debt Minimization Plan",
    settleUpSubtitle: "Algorithm optimizes debts into the minimal number of transactions:",
    noDebtsAllSettled: "🎉 Everyone is settled up! No transactions needed.",
    btnRecordPay: "Mark as Paid",
    payerPaysPayee: "pays",

    // Analytics Tab
    titleAnalytics: "Group Spending Analytics",
    cardTotalSpent: "Total Group Spending",
    cardAvgExpense: "Average Expense",
    cardTopCategory: "Top Category",
    cardExpenseCount: "Total Transactions",
    titleCategoryBreakdown: "Category Breakdown",
    titleTopSpenders: "Top Spenders",
    titleMonthlyTrends: "Monthly Dynamics",

    // Alerts & Notifications
    alertGroupCreated: "Group created successfully!",
    alertMemberAdded: "Member added successfully!",
    alertExpenseAdded: "Expense added successfully!",
    alertSettlementRecorded: "Settlement payment recorded successfully!",
    alertExpenseDeleted: "Expense deleted.",
    errorGeneric: "An error occurred. Please try again."
  },
  ru: {
    appName: "Dolg API",
    tagline: "Умный сервис учета групповых расходов и оптимизации долгов",
    langButton: "🇬🇧 ENG",
    navDocs: "Swagger API Docs",
    navGithub: "GitHub репозиторий",
    authTitle: "Добро пожаловать в Dolg",
    authSubtitle: "Войдите или зарегистрируйтесь для управления совместными расходами",
    tabLogin: "Вход",
    tabRegister: "Регистрация",
    labelEmail: "Email адрес",
    labelPassword: "Пароль",
    labelName: "Полное имя",
    btnLogin: "Войти",
    btnRegister: "Зарегистрироваться",
    lblLoggedInAs: "Вы вошли как",
    btnLogout: "Выйти",
    
    // Groups Section
    titleGroups: "Ваши группы",
    btnCreateGroup: "+ Создать группу",
    groupMembers: "участников",
    groupOwner: "Владелец",
    noGroupsYet: "Вы пока не состоите ни в одной группе. Создайте первую!",
    
    // Create Group Modal/Form
    modalCreateGroupTitle: "Создание группы расходов",
    labelGroupName: "Название группы",
    labelGroupDesc: "Описание (опционально)",
    phGroupName: "Например: Поездка в Алматы",
    phGroupDesc: "Например: Общий бюджет на продукты и отель",
    btnSubmitGroup: "Создать группу",
    btnCancel: "Отмена",
    
    // Group Dashboard View
    btnBackGroups: "← К списку групп",
    tabExpenses: "Расходы",
    tabBalance: "Баланс и Переводы",
    tabAnalytics: "Аналитика",
    
    // Add Member
    btnAddMember: "+ Добавить участника",
    phMemberEmail: "Email нового участника",
    btnSubmitMember: "Добавить",

    // Expenses Tab
    titleAddExpense: "Добавить расход",
    labelExpenseDesc: "Описание расхода",
    phExpenseDesc: "Например: Ужин в ресторане",
    labelExpenseAmount: "Сумма (₸ / $)",
    labelExpenseCategory: "Категория",
    labelSplitType: "Тип деления",
    splitEqual: "Поровну между всеми",
    splitExact: "Точные суммы",
    btnSubmitExpense: "Добавить расход",
    titleExpensesHistory: "История расходов",
    noExpensesYet: "В этой группе пока нет расходов.",
    paidBy: "оплатил(а)",
    splitEquallyAmong: "разделено на",
    deleteExpense: "Удалить",

    // Balance Tab
    titleGroupBalance: "Обзор чистых балансов",
    colMember: "Участник",
    colPaid: "Всего оплатил",
    colOwed: "Должен за покупки",
    colSettledNet: "Выплачено/Получено",
    colNetBalance: "Итоговый баланс",
    statusOwedToYou: "Вам должны",
    statusYouOwe: "Вы должны",
    statusSettled: "Все расчитаны",
    
    titleSettleUpPlan: "План взаиморасчётов (Жадный алгоритм)",
    settleUpSubtitle: "Алгоритм минимизирует количество переводов до наименьшего возможного:",
    noDebtsAllSettled: "🎉 Все долги закрыты! Переводы не требуются.",
    btnRecordPay: "Отметить оплаченным",
    payerPaysPayee: "переводит",

    // Analytics Tab
    titleAnalytics: "Аналитика расходов группы",
    cardTotalSpent: "Всего потрачено",
    cardAvgExpense: "Средний чек",
    cardTopCategory: "Главная категория",
    cardExpenseCount: "Всего транзакций",
    titleCategoryBreakdown: "Расходы по категориям",
    titleTopSpenders: "Топ плательщиков",
    titleMonthlyTrends: "Динамика по месяцам",

    // Alerts & Notifications
    alertGroupCreated: "Группа успешно создана!",
    alertMemberAdded: "Участник успешно добавлен!",
    alertExpenseAdded: "Расход успешно добавлен!",
    alertSettlementRecorded: "Перевод успешно зафиксирован!",
    alertExpenseDeleted: "Расход удален.",
    errorGeneric: "Произошла ошибка. Попробуйте еще раз."
  }
};

let currentLang = localStorage.getItem("dolg_lang") || "ru";

function getLang() {
  return currentLang;
}

function t(key) {
  if (translations[currentLang] && translations[currentLang][key]) {
    return translations[currentLang][key];
  }
  return translations["en"][key] || key;
}

function toggleLanguage() {
  currentLang = currentLang === "ru" ? "en" : "ru";
  localStorage.setItem("dolg_lang", currentLang);
  updateUILanguage();
}

function updateUILanguage() {
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    if (key) {
      el.textContent = t(key);
    }
  });

  document.querySelectorAll("[data-i18n-ph]").forEach((el) => {
    const key = el.getAttribute("data-i18n-ph");
    if (key) {
      el.setAttribute("placeholder", t(key));
    }
  });

  const langBtn = document.getElementById("langToggleBtn");
  if (langBtn) {
    langBtn.textContent = t("langButton");
  }

  // Trigger custom event for app logic if needed
  window.dispatchEvent(new CustomEvent("languageChanged", { detail: { lang: currentLang } }));
}
