// setup canvas

const canvas = document.querySelector("canvas");
const ctx = canvas.getContext("2d");

const width = (canvas.width = window.innerWidth);
const height = (canvas.height = window.innerHeight);

// function to generate random number

function random(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

// function to generate random color

function randomRGB() {
  return `rgb(${random(0, 255)},${random(0, 255)},${random(0, 255)})`;
}

const dice = [];

for (let x=0; x<5; x++) {
  const size = 50;
  const die = new Die(
    10 + x*(size+10),
    10,
    'red',
    size,
  );

  dice.push(die);
}

function loop() {
    ctx.fillStyle = "rgb(150 250 150 / 25%)";
    ctx.fillRect(0, 0, width, height);
  
    for (const die of dice) {
        die.draw();
        die.update();
    }
  
    requestAnimationFrame(loop);
}

loop();