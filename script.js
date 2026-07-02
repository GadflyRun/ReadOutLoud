function inferRepoUrls() {
  const { hostname, pathname } = window.location;

  if (hostname.endsWith(".github.io")) {
    const owner = hostname.replace(/\.github\.io$/, "");
    const parts = pathname.split("/").filter(Boolean);
    const repo = parts[0] || `${owner}.github.io`;
    const base = `https://github.com/${owner}/${repo}`;

    return {
      repoUrl: base,
      releaseUrl: `${base}/releases/latest`,
    };
  }

  return {
    repoUrl: "#top",
    releaseUrl: "#download",
  };
}

function hydrateLinks() {
  const links = inferRepoUrls();

  document.querySelectorAll("[data-link='repo']").forEach((node) => {
    node.href = links.repoUrl;
    if (links.repoUrl.startsWith("https://")) {
      node.target = "_blank";
      node.rel = "noreferrer";
    }
  });

  document.querySelectorAll("[data-link='release']").forEach((node) => {
    node.href = links.releaseUrl;
    if (links.releaseUrl.startsWith("https://")) {
      node.target = "_blank";
      node.rel = "noreferrer";
    }
  });
}

function bindHeaderState() {
  const header = document.querySelector("[data-header]");
  if (!header) return;

  const syncHeader = () => {
    header.classList.toggle("is-scrolled", window.scrollY > 12);
  };

  syncHeader();
  window.addEventListener("scroll", syncHeader, { passive: true });
}

function bindSectionHighlight() {
  const navLinks = Array.from(document.querySelectorAll(".site-nav a"));
  const sections = navLinks
    .map((link) => document.querySelector(link.getAttribute("href")))
    .filter(Boolean);

  if (!navLinks.length || !sections.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const id = `#${entry.target.id}`;
        navLinks.forEach((link) => {
          link.classList.toggle("is-active", link.getAttribute("href") === id);
        });
      });
    },
    {
      rootMargin: "-30% 0px -55% 0px",
      threshold: 0.01,
    }
  );

  sections.forEach((section) => observer.observe(section));
}

hydrateLinks();
bindHeaderState();
bindSectionHighlight();
