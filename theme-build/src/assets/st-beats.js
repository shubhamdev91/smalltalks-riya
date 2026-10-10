/**
 * Journal story beats: a native scroll-snap track enhanced with previous/next buttons, a polite
 * "n / N" status and ArrowLeft/ArrowRight on the focused track. Swipe works without this script.
 */
class StBeats extends HTMLElement {
  /** @type {AbortController | undefined} */
  #controller;
  /** @type {IntersectionObserver | undefined} */
  #observer;
  #index = 0;

  connectedCallback() {
    this.#controller = new AbortController();
    const { signal } = this.#controller;
    const track = this.track;
    if (!track) return;

    this.querySelector('[data-st-beats-prev]')?.addEventListener('click', () => this.go(this.#index - 1), { signal });
    this.querySelector('[data-st-beats-next]')?.addEventListener('click', () => this.go(this.#index + 1), { signal });
    track.addEventListener('keydown', this.#onKeyDown, { signal });

    this.#observer = new IntersectionObserver(this.#onIntersect, { root: track, threshold: 0.6 });
    for (const slide of this.slides) this.#observer.observe(slide);
  }

  disconnectedCallback() {
    this.#controller?.abort();
    this.#observer?.disconnect();
  }

  /** @returns {HTMLElement | null} */
  get track() {
    return this.querySelector('[data-st-beats-track]');
  }

  /** @returns {HTMLElement[]} */
  get slides() {
    return /** @type {HTMLElement[]} */ ([...(this.track?.children ?? [])]);
  }

  /** @param {number} index */
  go(index) {
    const slides = this.slides;
    const target = slides[Math.max(0, Math.min(slides.length - 1, index))];
    if (!target || !this.track) return;
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    this.track.scrollTo({ left: target.offsetLeft - this.track.offsetLeft, behavior: reduce ? 'auto' : 'smooth' });
  }

  /** @param {KeyboardEvent} event */
  #onKeyDown = (event) => {
    if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
    event.preventDefault();
    const forward = (event.key === 'ArrowRight') !== (document.dir === 'rtl');
    this.go(this.#index + (forward ? 1 : -1));
  };

  /** @param {IntersectionObserverEntry[]} entries */
  #onIntersect = (entries) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      const index = this.slides.indexOf(/** @type {HTMLElement} */ (entry.target));
      if (index === -1 || index === this.#index) continue;
      this.#index = index;
      this.#render();
    }
  };

  #render() {
    const count = this.slides.length;
    const status = this.querySelector('[data-st-beats-status]');
    if (status) status.textContent = `${this.#index + 1} / ${count}`;
    const prev = /** @type {HTMLButtonElement | null} */ (this.querySelector('[data-st-beats-prev]'));
    const next = /** @type {HTMLButtonElement | null} */ (this.querySelector('[data-st-beats-next]'));
    if (prev) prev.disabled = this.#index === 0;
    if (next) next.disabled = this.#index >= count - 1;
  }
}

if (!customElements.get('st-beats')) {
  customElements.define('st-beats', StBeats);
}
