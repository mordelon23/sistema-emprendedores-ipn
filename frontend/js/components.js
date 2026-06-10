// Genera la barra superior con el switcher de rol
function renderTopBar(currentRole = "comprador") {
  const user = Auth.getUser();
  if (!user) return "";
  return `
    <div class="top-bar">
      <h1>Emprendedores IPN</h1>
      <div class="role-switcher">
        <button id="rolComprador" class="${currentRole === 'comprador' ? 'active' : ''}">Comprador</button>
        <button id="rolEmprendedor" class="${currentRole === 'emprendedor' ? 'active' : ''}">Emprendedor</button>
      </div>
    </div>
  `;
}

// Genera la barra inferior de navegación
function renderBottomNav(activePage = "feed") {
  const role = Auth.getRole();
  const user = Auth.getUser();
  const isAdmin = user && user.is_admin;

  let items = [
    { id: "feed", label: "Inicio", icon: "🏠", href: "feed.html" },
    { id: "categories", label: "Categorías", icon: "📂", href: "categories.html" },
  ];

  if (role === "emprendedor") {
    items.push({ id: "create", label: "Publicar", icon: "➕", href: "create.html" });
  } else {
    items.push({ id: "favorites", label: "Favoritos", icon: "❤️", href: "favorites.html" });
  }
  items.push({ id: "profile", label: "Perfil", icon: "👤", href: "profile.html" });
  if (isAdmin) {
    items.push({ id: "admin", label: "Admin", icon: "⚙️", href: "admin.html" });
  }

  return `
    <div class="bottom-nav">
      ${items.map(i => `
        <a href="${i.href}" class="${activePage === i.id ? 'active' : ''}">
          <span class="icon">${i.icon}</span>
          <span>${i.label}</span>
        </a>
      `).join("")}
    </div>
  `;
}

// Activa los listeners del switcher de rol
function bindRoleSwitcher() {
  const btnC = document.getElementById("rolComprador");
  const btnE = document.getElementById("rolEmprendedor");
  if (btnC) btnC.addEventListener("click", () => { Auth.setRole("comprador"); location.reload(); });
  if (btnE) btnE.addEventListener("click", () => { Auth.setRole("emprendedor"); location.reload(); });
}

// Categorías y sus íconos
const CATEGORIAS = {
  dulces: { nombre: "Dulces", icon: "🍬" },
  comida: { nombre: "Comida", icon: "🍔" },
  accesorios: { nombre: "Accesorios", icon: "👜" },
  materiales_electronicos: { nombre: "Materiales electrónicos", icon: "🔌" },
  articulos_electronicos: { nombre: "Artículos electrónicos", icon: "📱" },
  otros: { nombre: "Otros", icon: "📦" },
};