document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;

      console.log(page);
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep++;
          this.updateForm();
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });

      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;

      // TODO: Validation

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

      // TODO: get data from inputs and show them in summary
      if (parseInt(document.getElementById('bags').value) === 1){
        document.getElementById('bagsPreview').innerHTML = document.getElementById('bags').value
      + " worek";
      } else if (parseInt(document.getElementById('bags').value) < 5){
        document.getElementById('bagsPreview').innerHTML = document.getElementById('bags').value
      + " worki";
      } else {
        document.getElementById('bagsPreview').innerHTML = document.getElementById('bags').value
      + " work??w";
      }
      if (document.getElementById('jedzenie').checked){
        document.getElementById('bagsPreview').innerHTML += " jedzenia";
      }
      if (document.getElementById('zabawki').checked){
        document.getElementById('bagsPreview').innerHTML += " zabawek";
      }
      if (document.getElementById('meble').checked){
        document.getElementById('bagsPreview').innerHTML += " mebli";
      }
      if (document.getElementById('ksi????ki').checked){
        document.getElementById('bagsPreview').innerHTML += " ksi????ek";
      }
      if (document.getElementById('ubrania').checked){
        document.getElementById('bagsPreview').innerHTML += " ubra??";
      }
      if (document.getElementById('Fundacja 1').checked){
        document.getElementById('institutionPreview').innerHTML = "Dla Fundacji 1";
      }
      if (document.getElementById('Fundacja 2').checked){
        document.getElementById('institutionPreview').innerHTML = "Dla Fundacji 2";
      }
      if (document.getElementById('Fundacja 3').checked){
        document.getElementById('institutionPreview').innerHTML = "Dla Fundacji 3";
      }
      if (document.getElementById('Fundacja 4').checked){
        document.getElementById('institutionPreview').innerHTML = "Dla Fundacji 4";
      }
      if (document.getElementById('Fundacja 5').checked){
        document.getElementById('institutionPreview').innerHTML = "Dla Fundacji 5";
      }
      if (document.getElementById('Fundacja 6').checked){
        document.getElementById('institutionPreview').innerHTML = "Dla Fundacji 6";
      }
      if (document.getElementById('Zbi??rka 1').checked){
        document.getElementById('institutionPreview').innerHTML = "Dla Zbi??rki 1";
      }
      if (document.getElementById('NGO 1').checked){
        document.getElementById('institutionPreview').innerHTML = "Dla NGO 1";
      }
      document.getElementById('streetPreview').innerHTML = document.getElementById('address').value;
      document.getElementById('cityPreview').innerHTML = document.getElementById('city').value;
      document.getElementById('postcodePreview').innerHTML = document.getElementById('postcode').value;
      document.getElementById('phonePreview').innerHTML = document.getElementById('phone').value;
      document.getElementById('datePreview').innerHTML = document.getElementById('date').value;
      document.getElementById('timePreview').innerHTML = document.getElementById('time').value;
      if (document.getElementById('extra').innerHTML != null){
        document.getElementById('extraPreview').innerHTML = document.getElementById('extra').value;
      }
      if (document.getElementById('extraPreview').innerHTML === ""){
        document.getElementById('extraPreview').innerHTML = "Brak uwag"
      }



    }

    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */
    submit(e) {
      e.preventDefault();
      const formData = new FormData(this.$form.getElementsByTagName('form').item(0));

      fetch('/make-donation/', {
        method: 'post',
        body: formData
      }).then(function (response) {
        return response.json();
      }).then(function (data) {
        window.location.href = data.myurl;
      }).catch(function (error) {
        console.error(error);
      })
      this.currentStep++;
      this.updateForm();
    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }
});
