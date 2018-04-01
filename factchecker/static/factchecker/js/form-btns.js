
$('.btn-group-toggle label').click( function() {

  if ( $(this).hasClass("active") == false ) {

    $(this).removeClass("btn-outline-info").addClass("btn-info");
    $(this).parent().find(".btn-info").removeClass("btn-info").addClass("btn-outline-info");

    $('#source-fields').find(".field-wrapper").toggleClass("hidden");
    $('.field-wrapper').filter('.hidden').find(".form-control").val("");
    $('.field-wrapper').filter('.hidden').find(".form-control").removeAttr("required");
  };

  if ( $(this).find("input").attr("id") == 'select' ) {
        
    $('#id_source').prop('required', true);

  } else if ( $(this).find("input").attr("id") == 'add-new' ) {

    $('#id_source_type').prop('required', true);
    $('#id_source_name').prop('required', true);

  };

});

$('#id_source_type option').click( function() {

  if ( $(this).val() == 'p' ) {
    $('#id_source_title').parent().removeClass("hidden");
  } else if ( $(this).val() == 'o' ) {
    $('#id_source_title').parent().addClass("hidden");
  }

});
