$(document).ready(function(){
    var $container = $('#container');

    $container.imagesLoaded( function(){
      $container.masonry({
        itemSelector : '.box'
      });
    });
})
