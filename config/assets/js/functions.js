init_game = function(ctx){

}

images = function(image){
    sprites = []
    var bg = new Image();
    for(img in image){
        bg.src = image
        sprites.push(bg)
    }

    return sprites
}

function loadImage(ctx, bg, x, y, w, h){
    ctx.drawImage(bg, x, y, w, h)
}

function layers(container, id, w, h){
    $("#"+container+"").append("<canvas id='"+id+"'>")
    $("#"+id+"").css({width: w, height: h})

    layer = document.getElementById(id);
    layer.width = window.innerWidth
    layer.height = window.innerHeight
    return layer.getContext('2d');
}