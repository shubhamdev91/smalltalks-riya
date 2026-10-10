/**
 * Keeps keyboard focus inside the Small Talk menu drawer while it is open.
 * The drawer is a native modal <dialog> opened by Horizon's DialogComponent; most browsers
 * already make the page inert, this wraps Tab/Shift+Tab at the edges so focus never leaves.
 */
class StFocusTrap extends HTMLElement {
  #controller = new AbortController();

  connectedCallback() {
    this.addEventListener('keydown', this.#onKeyDown, { signal: this.#controller.signal });
  }

  disconnectedCallback() {
    this.#controller.abort();
    this.#controller = new AbortController();
  }

  /** @param {KeyboardEvent} event */
  #onKeyDown = (event) => {
    if (event.key !== 'Tab') return;

    const focusable = [
      ...this.querySelectorAll('a[href], button:not([disabled]), input:not([disabled]), [tabindex]:not([tabindex="-1"])'),
    ].filter((element) => element instanceof HTMLElement && element.offsetParent !== null);
    if (focusable.length === 0) return;

    const first = focusable[0];
    const last = focusable[focusable.length - 1];

    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  };
}

if (!customElements.get('st-focus-trap')) {
  customElements.define('st-focus-trap', StFocusTrap);
}
