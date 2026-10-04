(() => {
  'use strict';
  const root = document.documentElement;
  const en = root.dataset.locale === 'en';
  const t = en ? {
    copy: 'Copy code', copied: 'Copied', copyFailed: 'Could not copy. Select the code to copy it.',
    loading: 'Loading documentation…', hint: 'Search pages, commands, and API guides.',
    none: 'No results. Try “install”, “starter”, or “auth”.', failed: 'Search could not load. Use the documentation menu.',
    results: count => `${count} results`, theme: value => `Theme: ${value}. Change theme`,
  } : {
    copy: '코드 복사', copied: '복사했어요', copyFailed: '복사하지 못했어요. 코드를 선택해 복사해 주세요.',
    loading: '문서를 불러오고 있어요…', hint: '문서, 명령어, API 가이드를 검색하세요.',
    none: '검색 결과가 없어요. 설치, starter, auth로 검색해 보세요.', failed: '검색을 불러오지 못했어요. 문서 메뉴를 이용해 주세요.',
    results: count => `검색 결과 ${count}개`, theme: value => `화면 테마: ${value}. 테마 변경`,
  };
  const themeNames = en ? { system: 'system', light: 'light', dark: 'dark' } : { system: '시스템', light: '밝게', dark: '어둡게' };
  const media = matchMedia('(prefers-color-scheme: dark)');
  const themeButtons = [...document.querySelectorAll('.theme-toggle')];
  const applyTheme = preference => {
    root.dataset.themePreference = preference;
    root.dataset.theme = preference === 'dark' || (preference === 'system' && media.matches) ? 'dark' : 'light';
    themeButtons.forEach(button => { const label = t.theme(themeNames[preference]); button.setAttribute('aria-label', label); button.title = label; });
  };
  applyTheme(root.dataset.themePreference || 'system');
  themeButtons.forEach(button => button.addEventListener('click', () => {
    const modes = ['system', 'light', 'dark'];
    const value = modes[(modes.indexOf(root.dataset.themePreference) + 1) % modes.length];
    applyTheme(value); try { localStorage.setItem('zuku-docs-theme', value); } catch {}
  }));
  media.addEventListener('change', () => { if (root.dataset.themePreference === 'system') applyTheme('system'); });

  const copyIcon = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="8" y="8" width="12" height="12" rx="2"></rect><path d="M16 8V4H4v12h4"></path></svg>';
  document.querySelectorAll('.prose pre').forEach(pre => {
    const code = pre.querySelector('code'); if (!code) return;
    const button = document.createElement('button'); button.type = 'button'; button.className = 'copy-button'; button.setAttribute('aria-label', t.copy); button.title = t.copy; button.innerHTML = copyIcon;
    button.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(code.textContent);
        button.dataset.copied = 'true'; button.setAttribute('aria-label', t.copied);
        document.getElementById('copy-announcement').textContent = t.copied;
        setTimeout(() => { delete button.dataset.copied; button.setAttribute('aria-label', t.copy); }, 1800);
      } catch { document.getElementById('copy-announcement').textContent = t.copyFailed; }
    });
    pre.append(button);
  });
  document.querySelectorAll('.prose table').forEach(table => {
    const wrap = document.createElement('div'); wrap.className = 'table-scroll'; wrap.tabIndex = 0; wrap.setAttribute('aria-label', en ? 'Scrollable table' : '가로로 이동할 수 있는 표');
    table.before(wrap); wrap.append(table);
  });
  document.querySelectorAll('.tabbed-set').forEach(group => {
    const inputs = [...group.querySelectorAll(':scope > input')];
    const labels = [...group.querySelectorAll('.tabbed-labels > label')];
    const blocks = [...group.querySelectorAll('.tabbed-content > .tabbed-block')];
    const list = group.querySelector('.tabbed-labels'); if (!list) return; list.setAttribute('role', 'tablist');
    const update = () => labels.forEach((label, i) => { label.setAttribute('aria-selected', String(Boolean(inputs[i]?.checked))); label.tabIndex = inputs[i]?.checked ? 0 : -1; });
    labels.forEach((label, i) => {
      label.id = `${inputs[i]?.id}-label`; label.setAttribute('role', 'tab');
      const panel = blocks[i]; if (panel) { panel.id = `${inputs[i]?.id}-panel`; panel.setAttribute('role', 'tabpanel'); panel.setAttribute('aria-labelledby', label.id); label.setAttribute('aria-controls', panel.id); }
      label.addEventListener('keydown', event => {
        if (!['ArrowLeft', 'ArrowRight', 'Home', 'End', ' ', 'Enter'].includes(event.key)) return;
        event.preventDefault(); const j = event.key === 'Home' ? 0 : event.key === 'End' ? labels.length - 1 : event.key === 'ArrowLeft' ? (i + labels.length - 1) % labels.length : event.key === 'ArrowRight' ? (i + 1) % labels.length : i;
        if (inputs[j]) inputs[j].checked = true; update(); labels[j]?.focus();
      });
    }); inputs.forEach(input => input.addEventListener('change', update)); update();
  });

  const dialog = document.getElementById('search-dialog');
  const input = document.getElementById('search-input');
  const status = document.getElementById('search-status');
  const results = document.getElementById('search-results');
  const menu = document.getElementById('navigation-dialog');
  let catalog; let loading; let activeIndex = -1; let resultLinks = [];
  const closeDialog = element => { element.close(); if (!dialog.open && !menu.open) document.body.classList.remove('modal-open'); };
  [dialog, menu].forEach(element => {
    element.addEventListener('close', () => { if (element === dialog) input.setAttribute('aria-expanded', 'false'); if (!dialog.open && !menu.open) document.body.classList.remove('modal-open'); });
    element.addEventListener('click', event => {
      if (event.target !== element) return; const box = element.getBoundingClientRect();
      if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) closeDialog(element);
    });
    element.querySelectorAll('[data-close-dialog]').forEach(button => button.addEventListener('click', () => closeDialog(element)));
  });
  const highlight = (element, text, query) => {
    const at = text.toLocaleLowerCase().indexOf(query.toLocaleLowerCase());
    if (at < 0 || !query) { element.textContent = text; return; }
    element.append(document.createTextNode(text.slice(0, at))); const mark = document.createElement('mark'); mark.textContent = text.slice(at, at + query.length); element.append(mark, document.createTextNode(text.slice(at + query.length)));
  };
  const select = index => {
    activeIndex = index; resultLinks.forEach((link, i) => link.setAttribute('aria-selected', String(i === index)));
    if (resultLinks[index]) { input.setAttribute('aria-activedescendant', resultLinks[index].id); resultLinks[index].scrollIntoView({ block: 'nearest' }); } else input.removeAttribute('aria-activedescendant');
  };
  const renderSearch = () => {
    if (!catalog) return; const query = input.value.trim().slice(0, 160); const lower = query.toLocaleLowerCase(); const words = lower.split(/\s+/).filter(Boolean);
    const matches = catalog.map(page => {
      const title = page.title.toLocaleLowerCase(); const text = page.text.toLocaleLowerCase();
      if (words.some(word => !title.includes(word) && !text.includes(word))) return null;
      return { page, score: !lower ? page.order : (title === lower ? -100 : title.includes(lower) ? -50 : words.filter(word => title.includes(word)).length * -10) };
    }).filter(Boolean).sort((a, b) => a.score - b.score || a.page.order - b.page.order).slice(0, 8);
    results.replaceChildren(); resultLinks = [];
    status.textContent = query ? matches.length ? t.results(matches.length) : t.none : t.hint;
    matches.forEach(({ page }, index) => {
      const link = document.createElement('a'); link.className = 'search-result'; link.href = page.url; link.id = `search-result-${index}`; link.setAttribute('role', 'option'); link.tabIndex = 0;
      const small = document.createElement('small'); small.textContent = page.section; const title = document.createElement('strong'); highlight(title, page.title, query);
      const summary = document.createElement('p'); const at = lower ? page.text.toLocaleLowerCase().indexOf(words[0] || '') : 0; const begin = Math.max(0, at - 48); const snippet = (begin ? '…' : '') + page.text.slice(begin, begin + 160) + (page.text.length > begin + 160 ? '…' : ''); highlight(summary, snippet, query);
      link.append(small, title, summary); link.addEventListener('pointermove', () => select(index)); resultLinks.push(link); results.append(link);
    }); results.setAttribute('role', 'listbox'); select(matches.length ? 0 : -1);
  };
  const loadCatalog = async () => {
    if (catalog) return;
    if (!loading) loading = (async () => {
      status.textContent = t.loading;
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), 8000);
      let response;
      try { response = await fetch(`/assets/search-${en ? 'en' : 'ko'}.json`, { credentials: 'omit', signal: controller.signal }); }
      finally { clearTimeout(timer); }
      if (!response.ok) throw new Error('search load'); const data = await response.json();
      if (!Array.isArray(data) || data.length > 300 || data.some(page => typeof page.title !== 'string' || typeof page.text !== 'string' || typeof page.url !== 'string' || !page.url.startsWith(en ? '/en/' : '/') || page.url.startsWith('//'))) throw new Error('search contract');
      catalog = data;
    })();
    try { await loading; } catch { loading = undefined; status.textContent = t.failed; }
  };
  const openSearch = async () => {
    if (menu.open) closeDialog(menu); if (!dialog.open) dialog.showModal(); document.body.classList.add('modal-open'); input.setAttribute('aria-expanded', 'true'); input.focus(); await loadCatalog(); if (dialog.open) renderSearch();
  };
  document.querySelectorAll('[data-open-search]').forEach(button => button.addEventListener('click', openSearch));
  document.querySelectorAll('[data-open-menu]').forEach(button => button.addEventListener('click', () => { if (dialog.open) closeDialog(dialog); menu.showModal(); document.body.classList.add('modal-open'); }));
  input.addEventListener('input', renderSearch);
  input.addEventListener('keydown', event => {
    if (event.key === 'ArrowDown' || event.key === 'ArrowUp') { event.preventDefault(); if (resultLinks.length) select((activeIndex + (event.key === 'ArrowDown' ? 1 : -1) + resultLinks.length) % resultLinks.length); }
    else if (event.key === 'Enter' && resultLinks[activeIndex]) { event.preventDefault(); resultLinks[activeIndex].click(); }
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && (dialog.open || menu.open)) { event.preventDefault(); closeDialog(dialog.open ? dialog : menu); return; }
    if ((event.ctrlKey || event.metaKey) && event.key.toLocaleLowerCase() === 'k') { event.preventDefault(); if (dialog.open) closeDialog(dialog); else openSearch(); }
  });
  document.querySelectorAll('.search-trigger kbd').forEach(kbd => { if (/Mac|iPhone|iPad/.test(navigator.platform)) kbd.textContent = '⌘ K'; });
  const headings = [...document.querySelectorAll('.prose h2[id],.prose h3[id]')];
  if ('IntersectionObserver' in window) {
    const tocLinks = [...document.querySelectorAll('.toc a[href^="#"]')];
    const observer = new IntersectionObserver(entries => {
      for (const entry of entries) if (entry.isIntersecting) tocLinks.forEach(link => { const current = decodeURIComponent(link.hash.slice(1)) === entry.target.id; link.classList.toggle('current', current); if (current) link.setAttribute('aria-current', 'location'); else link.removeAttribute('aria-current'); });
    }, { rootMargin: '-90px 0px -65% 0px' }); headings.forEach(heading => observer.observe(heading));
  }
})();
