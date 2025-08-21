/* Javascript for CustomImageEditBlock. */
function CustomImageEditBlock(runtime, element) {
  var submitButton = $("#image-submit-options", element);
  var cancelButton = $("#cancel_button", element);
  var errorMessage = $(".xblock-editor-error-message", element);
  var validationAlert = $(".validation_alert", element);

  // Form fields
  var displayNameField = $("#edit_display_name", element);
  var imageUrlField = $("#edit_image_url", element);
  var imageAltField = $("#edit_image_alt", element);

  // Clear buttons
  var clearDisplayNameButton = $(".clear-display-name", element);

  function validateForm() {
    var isValid = true;
    var errors = [];

    // Reset validation state
    $(".setting-input", element).removeClass("error");
    validationAlert.addClass("covered");
    errorMessage.text("");

    // Validate display name
    if (!displayNameField.val().trim()) {
      errors.push("Display name is required");
      displayNameField.addClass("error");
      isValid = false;
    }

    // Validate image URL
    var imageUrl = imageUrlField.val().trim();
    if (!imageUrl) {
      errors.push("Image URL is required");
      imageUrlField.addClass("error");
      isValid = false;
    } else {
      // Basic URL validation
      var urlPattern = /^https?:\/\/.+/;
      if (!urlPattern.test(imageUrl)) {
        errors.push("Please enter a valid HTTP or HTTPS URL");
        imageUrlField.addClass("error");
        isValid = false;
      }
    }

    if (!isValid) {
      validationAlert.removeClass("covered");
      errorMessage.text(errors.join(", "));
    }

    return isValid;
  }

  function submitForm() {
    if (!validateForm()) {
      return;
    }

    var data = {
      display_name: displayNameField.val().trim(),
      image_url: imageUrlField.val().trim(),
      image_alt: imageAltField.val().trim(),
    };

    $.ajax({
      type: "POST",
      url: runtime.handlerUrl(element, "studio_submit"),
      data: JSON.stringify(data),
      success: function (response) {
        if (response.result === "success") {
          // Close the editor
          runtime.notify("save", { state: "end" });
        } else {
          errorMessage.text("Failed to save changes. Please try again.");
        }
      },
      error: function () {
        errorMessage.text("An error occurred while saving. Please try again.");
      },
    });
  }

  function cancelEdit() {
    runtime.notify("cancel", {});
  }

  function clearDisplayName() {
    var defaultValue = displayNameField.attr("data-default-value");
    displayNameField.val(defaultValue);
    displayNameField.removeClass("error");
  }

  // Event handlers
  submitButton.click(function (e) {
    e.preventDefault();
    submitForm();
  });

  cancelButton.click(function (e) {
    e.preventDefault();
    cancelEdit();
  });

  clearDisplayNameButton.click(function (e) {
    e.preventDefault();
    clearDisplayName();
  });

  // Real-time validation
  $(".setting-input", element).on("input blur", function () {
    $(this).removeClass("error");
    if (validationAlert.hasClass("covered") === false) {
      // Re-validate if validation alert is showing
      setTimeout(validateForm, 100);
    }
  });

  // URL preview functionality
  imageUrlField.on("blur", function () {
    var url = $(this).val().trim();
    if (url && url.match(/^https?:\/\/.+\.(jpg|jpeg|png|gif|svg|webp)$/i)) {
      // Could add image preview functionality here
      console.log("Valid image URL detected:", url);
    }
  });
}
