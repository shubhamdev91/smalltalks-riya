// Small Talk forms (help, Start a talk, the talks reply box): register validation messages and the "Sending…" state.
// Messages come from data attributes rendered from locale (small_talk.forms.*), so no copy lives here.
// Without JavaScript the forms still submit and Shopify's server-side errors are shown by the Liquid.

for (const form of document.querySelectorAll('form[data-st-form]')) {
  const messages = form.querySelector('[data-msg-required]')?.dataset ?? {};

  /** @param {HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement} field */
  const messageFor = (field) => {
    const kind = field.dataset.msg;
    if (field.validity.valueMissing) {
      if (kind === 'email') return messages.msgEmailMissing;
      if (kind === 'name-missing') return messages.msgNameMissing;
      if (kind === 'message-missing') return messages.msgMessageMissing;
      if (kind === 'topic-missing') return messages.msgTopicMissing;
      return messages.msgRequired;
    }
    if (field.validity.typeMismatch && kind === 'email') return messages.msgEmailInvalid;
    if (field.validity.tooLong && messages.msgTooLong) {
      return messages.msgTooLong.replace('{max}', String(field.maxLength));
    }
    return messages.msgRequired;
  };

  form.addEventListener('submit', (event) => {
    const fields = /** @type {NodeListOf<HTMLInputElement>} */ (form.querySelectorAll('input, textarea, select'));
    let first = null;
    for (const field of fields) {
      field.setCustomValidity('');
      const error = field.parentElement?.querySelector('.st-field__error');
      error?.remove();
      field.removeAttribute('aria-invalid');
      if (field.dataset.describedby) field.setAttribute('aria-describedby', field.dataset.describedby);
      else field.removeAttribute('aria-describedby');
      if (!field.checkValidity()) {
        const text = messageFor(field);
        const note = document.createElement('span');
        note.className = 'st-field__error';
        note.id = `${field.name.replace(/\W/g, '')}-error`;
        note.textContent = text ?? '';
        field.after(note);
        field.setAttribute('aria-invalid', 'true');
        field.setAttribute('aria-describedby', [note.id, field.dataset.describedby].filter(Boolean).join(' '));
        first ??= field;
      }
    }
    if (first) {
      event.preventDefault();
      // Reveal fields a compact form keeps folded (the talks reply box) before focusing the first problem.
      form.querySelector('[data-msg-required]')?.toggleAttribute('data-st-open', true);
      first.focus();
      return;
    }
    const button = form.querySelector('button[type="submit"][data-sending]');
    if (button instanceof HTMLButtonElement) {
      // Icon-only buttons keep their icon; the sending text goes to the form's status region instead.
      const status = form.querySelector('[data-st-status]');
      if (status) status.textContent = button.dataset.sending ?? '';
      else button.textContent = button.dataset.sending ?? button.textContent;
      button.setAttribute('aria-disabled', 'true');
    }
  });

  form.querySelector('[data-st-form-summary]')?.focus();
}
