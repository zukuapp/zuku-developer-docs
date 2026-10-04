(() => {
  let preference = 'system';
  try { const value = localStorage.getItem('zuku-docs-theme'); if (['light', 'dark', 'system'].includes(value)) preference = value; } catch {}
  const dark = preference === 'dark' || (preference === 'system' && matchMedia('(prefers-color-scheme: dark)').matches);
  document.documentElement.dataset.theme = dark ? 'dark' : 'light';
  document.documentElement.dataset.themePreference = preference;
})();
