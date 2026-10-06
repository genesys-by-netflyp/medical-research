/* Shared auth + nav module for the medical preprint site.
   Loads after the supabase-js v2 script tag. Exposes window.Auth = {sb, currentUser, getProfile, injectNav}.
   NOTE: SUPABASE_ANON_KEY below must be the real public anon key (same value review.html uses).
   The stored copy is currently a masked placeholder — replace before deploying. */
window.Auth = (function () {
  const SUPABASE_URL = "https://zihmokjuleecudhjmsyw.supabase.co";
  const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InppaG1va2p1bGVlY3VkaGptc3l3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTA1ODE0ODAsImV4cCI6MjEwNjE1NzQ4MH0.p262PYnfC0r-Mk7pZm4G1Bwsoa8g0DVCB_cFqINXDEE"; // public anon key — same literal as review.html

  const sb = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

  async function currentUser() {
    const { data } = await sb.auth.getUser();
    return (data && data.user) || null;
  }

  async function getProfile() {
    const user = await currentUser();
    if (!user) return null;
    const { data, error } = await sb.from("profiles").select("*").eq("id", user.id).maybeSingle();
    if (error) { console.error("getProfile:", error); return null; }
    return data;
  }

  /* Injects a site-wide header nav with links + login/logout toggle. */
  async function injectNav(active) {
    const user = await currentUser();
    const el = document.createElement("div");
    el.style.cssText = "max-width:760px;margin:0 auto;";
    el.innerHTML =
      '<nav style="font-size:.85rem;border-bottom:1px solid #ccc;padding-bottom:.5rem;margin-bottom:1.2rem">' +
      '<a href="/index.html">Home</a> &nbsp;·&nbsp; <a href="/dashboard.html">Dashboard</a> &nbsp;·&nbsp; ' +
      '<a href="/review.html">Submit a review</a> &nbsp;·&nbsp; <a href="/reviewers.html">Reviewers</a>' +
      '<span style="float:right"><a href="#" id="nav-auth">' + (user ? "Logout" : "Login") + "</a></span>" +
      "</nav>";
    document.body.insertBefore(el, document.body.firstChild);
    document.getElementById("nav-auth").addEventListener("click", async (e) => {
      e.preventDefault();
      if (user) {
        await sb.auth.signOut();
        window.location.href = "/index.html";
      } else {
        window.location.href = "/login.html";
      }
    });
    return user;
  }

  /* Guard for pages that require login: redirect to login.html when signed out. */
  async function requireLogin() {
    const user = await currentUser();
    if (!user) { window.location.href = "/login.html?next=" + encodeURIComponent(window.location.pathname + window.location.search); }
    return user;
  }

  return { sb, currentUser, getProfile, injectNav, requireLogin };
})();
