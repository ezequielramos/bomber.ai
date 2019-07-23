window.onload = async () => {

    function delay(time) {
        return new Promise((resolve, reject) => setTimeout(resolve, time));
    }

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

    function clear_object_list(raw_line) {
        const objects_aux = raw_line.split(' ');
        const objects = [];
        for (const _object of objects_aux) {
            [x, y] = _object.split(',');
            objects.push({ x, y });
        }
        return objects;
    }

    window.openFile = function (event) {
        const input = event.target;

        const reader = new FileReader();
        reader.onload = async () => {
            const text = reader.result;
            const line_by_line = text.split('\n');

            let map_size = line_by_line.splice(0, 1)[0];

            [width, height] = map_size.split(',');
            map_size = { width, height };

            let walls = line_by_line.splice(0, 1)[0];

            walls_aux = walls.split(' ');
            walls = [];
            for (const wall of walls_aux) {
                [x, y] = wall.split(',');
                walls.push({ x, y });
            }

            const players = [];
            let player = line_by_line.splice(0, 1);
            while (player != "") {
                players.push(player);
                player = line_by_line.splice(0, 1);
            }

            let turn_objects = line_by_line.splice(0, 4);
            turn = 1;

            while (turn_objects.length == 4) {
                let blocks = clear_object_list(turn_objects[0]);
                let explosions = clear_object_list(turn_objects[1]);
                let bombs = clear_object_list(turn_objects[2]);
                let bots = clear_object_list(turn_objects[3]);

                drawCanvas(map_size, walls, blocks, explosions, bombs, bots, players);
                turn_objects = line_by_line.splice(0, 4);
                turn += 1;
                await delay(100);
            }
        };
        reader.readAsText(input.files[0]);
    };

    function drawCanvas(map_size, walls, blocks, explosions, bombs, bots, players) {


        const c = document.getElementById("myCanvas");
        const ctx = c.getContext("2d");

        for (var x = 0; x < map_size.width - (-2); x++) {
            ctx.drawImage(wall, 50 * x, 0);
            ctx.drawImage(wall, 50 * x, (map_size.height - (-1)) * 50);
        }

        for (var y = 0; y < map_size.height - (-2); y++) {
            ctx.drawImage(wall, 0, 50 * y);
            ctx.drawImage(wall, (map_size.width - (-1)) * 50, 50 * y);
        }

        for (var x = 1; x < map_size.width - (-1); x++) {
            for (var y = 1; y < map_size.height - (-1); y++) {
                ctx.drawImage(emptyspace, 50 * x, 50 * y);
            }
        }

        for (const object of walls) {
            ctx.drawImage(wall, 50 * (object.x - (-1)), 50 * (object.y - (-1)));
        }

        for (const object of blocks) {
            ctx.drawImage(block, 50 * (object.x - (-1)), 50 * (object.y - (-1)));
        }

        for (const object of explosions) {
            ctx.drawImage(explosion, 50 * (object.x - (-1)), 50 * (object.y - (-1)));
        }

        for (const object of bombs) {
            ctx.drawImage(bomb, 50 * (object.x - (-1)), 50 * (object.y - (-1)));
        }

        for (const object of bots) {
            ctx.drawImage(bomberai, 50 * (object.x - (-1)), (50 * (object.y - (-1))) - 20);
        }

    }


};