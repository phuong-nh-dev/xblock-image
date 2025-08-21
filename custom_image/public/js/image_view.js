/* Javascript for CustomImageBlock. */
function CustomImageBlock(runtime, element) {
  var image = $("img.image-display", element);
  var xblock_wrapper = $(".image-xblock-wrapper", element);
  var display_name = xblock_wrapper.attr("data-display-name");
  var image_url = xblock_wrapper.attr("data-image-url");
  var image_alt = xblock_wrapper.attr("data-image-alt");

  // Set proper alt text
  if (image.length > 0) {
    var alt_text = image_alt || display_name || "Image";
    image.attr("alt", alt_text);
    image.attr("title", display_name);
  }

  function SignalImageLoaded(ev) {
    var image_src = $(ev.target).attr("src");
    $.ajax({
      type: "POST",
      url: runtime.handlerUrl(element, "publish_event"),
      data: JSON.stringify({
        url: image_src,
        event_type: "edx.custom_image.displayed",
        display_name: display_name,
      }),
      success: function () {
        $(".load_event_complete", element).val(
          "I've published the event that indicates that the image load has completed"
        );
      },
    });
  }

  function SignalImageError(ev) {
    console.error("Failed to load image:", $(ev.target).attr("src"));
    $.ajax({
      type: "POST",
      url: runtime.handlerUrl(element, "publish_event"),
      data: JSON.stringify({
        url: $(ev.target).attr("src"),
        event_type: "edx.custom_image.load_error",
        display_name: display_name,
      }),
    });
  }

  // Bind events
  image.on("load", SignalImageLoaded);
  image.on("error", SignalImageError);

  // Add loading class management
  image.addClass("loading");
  image.on("load", function () {
    $(this).removeClass("loading");
  });
}
