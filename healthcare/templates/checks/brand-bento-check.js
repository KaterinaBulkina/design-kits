() => {
  const r = [];
  document.querySelectorAll('.chip,.serif,.sc div').forEach(e => {
    if (e.scrollWidth > e.clientWidth + 1 || e.scrollHeight > e.clientHeight + 2)
      r.push(e.textContent.trim().slice(0, 25) + ' ' + e.scrollWidth + 'x' + e.scrollHeight + ' / ' + e.clientWidth + 'x' + e.clientHeight);
  });
  return r;
}
