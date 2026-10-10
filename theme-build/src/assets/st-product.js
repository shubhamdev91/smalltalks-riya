/**
 * Adds ArrowLeft / ArrowRight to Horizon's product media gallery when focus is inside it.
 * Uses the slideshow component's own previous()/next(); thumbnails and arrow buttons stay native.
 */
const handleKeydown = (event) => {
  if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
  if (!(event.target instanceof Element)) return;
  if (event.target.closest('input, textarea, select, [contenteditable]')) return;

  const slideshow = event.target.closest('media-gallery slideshow-component');
  if (!slideshow || typeof slideshow.next !== 'function') return;

  event.preventDefault();
  const forward = (event.key === 'ArrowRight') !== (document.dir === 'rtl');
  if (forward) slideshow.next();
  else slideshow.previous();
};

if (!window.stGalleryKeys) {
  window.stGalleryKeys = true;
  document.addEventListener('keydown', handleKeydown);
}
