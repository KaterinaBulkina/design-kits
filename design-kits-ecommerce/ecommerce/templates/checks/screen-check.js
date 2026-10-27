() => {
  // 1. text that does not fit its box
  const bad = [];
  document.querySelectorAll('.btn2,.cta,.chip,.fi,.bdg,.tagp,.rt .ch,.srch,.q,.sel,.sel2,.ad,.vc').forEach(e => {
    if (e.scrollWidth > e.clientWidth + 1) bad.push(e.textContent.trim().slice(0, 30) + ' ' + e.scrollWidth + '>' + e.clientWidth);
  });
  // 2. broken images (wrong file name or missing photo)
  const broken = [...document.images].filter(i => !i.complete || !i.naturalWidth).map(i => i.getAttribute('src').slice(0, 40));
  // 3. key controls must be fully inside the page area (nothing clipped by the window)
  const pg = document.getElementById('pg').getBoundingClientRect();
  const clipped = [];
  document.querySelectorAll('.cta,.mf .p,.fa,.df .vc,.tot,.add').forEach(e => {
    const r = e.getBoundingClientRect();
    if (r.width && (r.bottom > pg.bottom - 8 || r.right > pg.right)) clipped.push(e.className + ' ' + Math.round(r.bottom) + '>' + Math.round(pg.bottom));
  });
  // 4. last list row or last block bottom vs page (cart page should not be clipped)
  const L = document.querySelector('.L');
  const lastRow = L ? Math.round(L.getBoundingClientRect().bottom) : null;
  return { bad, broken, clipped, pageBottom: Math.round(pg.bottom), listBottom: lastRow };
}
