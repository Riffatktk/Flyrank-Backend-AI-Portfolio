/**
 * Embeddable widget loader.
 * Usage on any external site:
 *   <script src="https://your-domain.com/widget.js?id=WIDGET_ID" async></script>
 *
 * This one file: reads its own <script> tag to find the widget id, fetches
 * the widget's config from the public config endpoint, renders a minimal
 * form, and posts submissions back -- including a hidden honeypot field.
 */
(function () {
  var API_BASE = (function () {
    var scripts = document.getElementsByTagName("script");
    var thisScript = scripts[scripts.length - 1];
    var src = thisScript.src;
    return src.substring(0, src.indexOf("/widget.js"));
  })();

  var params = new URLSearchParams(
    document.currentScript ? document.currentScript.src.split("?")[1] : ""
  );
  var widgetId = params.get("id");
  if (!widgetId) {
    console.error("[widget] missing ?id= on the script tag");
    return;
  }

  fetch(API_BASE + "/widgets/" + widgetId + "/config")
    .then(function (r) { return r.json(); })
    .then(renderWidget)
    .catch(function (err) { console.error("[widget] failed to load config", err); });

  function renderWidget(config) {
    var container = document.createElement("div");
    container.className = "embedded-widget";
    container.style.cssText =
      "max-width:320px;padding:16px;border:1px solid #ddd;border-radius:8px;font-family:sans-serif;";

    var title = document.createElement("h3");
    title.textContent = config.title;
    container.appendChild(title);

    if (config.description) {
      var desc = document.createElement("p");
      desc.textContent = config.description;
      container.appendChild(desc);
    }

    var form = document.createElement("form");

    (config.fields || []).forEach(function (fieldName) {
      var input = document.createElement("input");
      input.type = fieldName === "email" ? "email" : "text";
      input.name = fieldName;
      input.placeholder = fieldName;
      input.required = true;
      input.style.cssText = "display:block;width:100%;margin-bottom:8px;padding:6px;";
      form.appendChild(input);
    });

    // Honeypot: hidden from real users via CSS, bots fill it anyway.
    var honeypot = document.createElement("input");
    honeypot.type = "text";
    honeypot.name = "website";
    honeypot.autocomplete = "off";
    honeypot.tabIndex = -1;
    honeypot.style.cssText = "position:absolute;left:-9999px;";
    form.appendChild(honeypot);

    var submitBtn = document.createElement("button");
    submitBtn.type = "submit";
    submitBtn.textContent = config.button_text || "Submit";
    form.appendChild(submitBtn);

    var status = document.createElement("p");
    status.style.fontSize = "13px";

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var formData = new FormData(form);
      var data = {};
      formData.forEach(function (value, key) {
        if (key !== "website") data[key] = value;
      });

      fetch(API_BASE + "/widgets/" + widgetId + "/submissions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ data: data, website: honeypot.value }),
      })
        .then(function (r) {
          if (!r.ok) throw new Error("submission failed: " + r.status);
          return r.json();
        })
        .then(function () {
          status.textContent = "Thanks! Submission received.";
          form.reset();
        })
        .catch(function (err) {
          status.textContent = "Something went wrong. Please try again.";
          console.error(err);
        });
    });

    container.appendChild(form);
    container.appendChild(status);

    document.currentScript
      ? document.currentScript.parentNode.insertBefore(container, document.currentScript.nextSibling)
      : document.body.appendChild(container);
  }
})();
