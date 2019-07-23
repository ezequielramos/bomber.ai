window.onload = async () => {

    function loadImages(src) {
        return new Promise((resolve, reject) => {
            const img = new Image(50, 50);
            img.src = src;
            img.onload = () => resolve(img);
            img.onerror = () => reject();
        });
    }

    const wall = await loadImages('images/wall.png');
    const emptyspace = await loadImages('images/emptyspace.png');
    const block = await loadImages('images/block.png');
    const bomb = await loadImages('images/bomb.png');
    const bomberai = await loadImages('images/bomber.ai.png');
    const explosion = await loadImages('images/explosion.png');

    var c = document.getElementById("myCanvas");
    var ctx = c.getContext("2d");

    for (var x = 0; x < 15; x++) {
        ctx.drawImage(wall, 50 * x, 0);
        ctx.drawImage(wall, 50 * x, 12 * 50);
    }

    for (var y = 0; y < 13; y++) {
        ctx.drawImage(wall, 0, 50 * y);
        ctx.drawImage(wall, 14 * 50, 50 * y);
    }

    for (var x = 1; x < 14; x++) {
        for (var y = 1; y < 12; y++) {
            ctx.drawImage(emptyspace, 50 * x, 50 * y);
        }
    }

    for (var x = 0; x < 14; x += 2) {
        for (var y = 0; y < 12; y += 2) {
            ctx.drawImage(wall, 50 * x, 50 * y);
        }
    }

    for (var x = 1; x < 14; x += 2) {
        for (var y = 1; y < 12; y += 2) {
            if (x == 1 && y == 1) {
                continue;
            }

            if (x == 1 && y == 1) {
                continue;
            }

            if (x == 11 && y == 11) {
                continue;
            }

            if (x == 13 && y == 11) {
                continue;
            }

            if (x == 13 && y == 9) {
                continue;
            }
            ctx.drawImage(block, 50 * x, 50 * y);
        }
    }

    ctx.drawImage(block, 50 * 3, 50 * 1);
    ctx.drawImage(block, 50 * 3, 50 * 3);
    ctx.drawImage(block, 50 * 1, 50 * 3);
    ctx.drawImage(block, 50 * 2, 50 * 3);
    ctx.drawImage(block, 50 * 3, 50 * 2);
    ctx.drawImage(bomb, 50 * 2, 50 * 1);
    ctx.drawImage(bomberai, 50 * 2, (50 * 1) - 20);



    ctx.drawImage(bomberai, 50 * 10, (50 * 11) - 20);
    ctx.drawImage(explosion, 50 * 13, 50 * 11);
    ctx.drawImage(explosion, 50 * 13, 50 * 10);
    ctx.drawImage(explosion, 50 * 13, 50 * 9);
    ctx.drawImage(explosion, 50 * 12, 50 * 11);
    ctx.drawImage(explosion, 50 * 11, 50 * 11);

    ctx.drawImage(block, 50 * 9, 50 * 11);
    ctx.drawImage(block, 50 * 9, 50 * 10);
    ctx.drawImage(block, 50 * 9, 50 * 9);
    ctx.drawImage(block, 50 * 10, 50 * 9);
    ctx.drawImage(block, 50 * 11, 50 * 9);
    ctx.drawImage(block, 50 * 12, 50 * 9);
    ctx.drawImage(block, 50 * 13, 50 * 8);




};