class Die {
    constructor(x, y, color, size) {
        this.x = x;
        this.y = y;
        this.color = color;
        this.size = size;
        this.color;
        this.roll();
    }

    roll() {
        this.value = Math.floor(Math.random()*6) + 1
    }

    update() {
        
    }

    draw() {
        ctx.beginPath();
        ctx.fillStyle = this.color;
        ctx.lineWidth = 1;
        ctx.strokeStyle = '#000000';
        ctx.roundRect(this.x, this.y, this.size, this.size, 7);
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = '#ffffff';
        ctx.font = "20px Arial, Helvetica, sans-serif";
        ctx.fillText(this.value.toString(), this.x+this.size/2-5, this.y+this.size/2+5);
    }
}