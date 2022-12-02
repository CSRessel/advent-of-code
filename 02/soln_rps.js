const input = document.body.textContent.trim();

var games = input.split("\n").map(e => e.split(" "));

// part 1
function getMoveScore(theirMove, ourMove) { return ourMove === "X" ? 1 : (ourMove === "Y" ? 2 : 3); }
function getGameScore(theirMove, ourMove) { return theirMove === "A" ? (ourMove === "X" ? 3 : (ourMove === "Y" ? 6 : 0)) : (theirMove === "B" ? (ourMove === "X" ? 0 : (ourMove === "Y" ? 3 : 6)) : (ourMove === "X" ? 6 : (ourMove === "Y" ? 0 : 3))); }
console.log(games.map(g => getGameScore(...g) + getMoveScore(...g)).reduce((partialSum, element) => partialSum + element));

// part 2
function getGameScore(theirMove, ourMove) { return ourMove === "X" ? 0 : (ourMove === "Y" ? 3 : 6); }
function getMoveScore(theirMove, ourMove) { return theirMove === "A" ? (ourMove === "X" ? 3 : (ourMove === "Y" ? 1 : 2)) : (theirMove === "B" ? (ourMove === "X" ? 1 : (ourMove === "Y" ? 2 : 3)) : (ourMove === "X" ? 2 : (ourMove === "Y" ? 3 : 1))); }
console.log(games.map(g => getGameScore(...g) + getMoveScore(...g)).reduce((partialSum, element) => partialSum + element));
