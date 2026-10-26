() => {
  const bad = [];
  document.querySelectorAll('.nav,.pill,.g>div,.btn,.field').forEach(e => {
    if (e.scrollWidth > e.clientWidth + 1) bad.push(e.textContent.trim().slice(0, 30) + ' ' + e.scrollWidth + '>' + e.clientWidth);
  });
  const pan = document.getElementById('pan');
  if (!pan) return { bad };
  const ch = [...pan.children], last = ch[ch.length - 1].getBoundingClientRect(), pr = pan.getBoundingClientRect();
  const g = ch.map(c => [Math.round(c.getBoundingClientRect().top), Math.round(c.getBoundingClientRect().bottom)]);
  return { bad, panBottom: pr.bottom, lastBottom: last.bottom, g };
}
