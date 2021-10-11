const x0 = -170;
const z0 = -196;
const x1 = -1144;
const z1 = +284;

const w0 = 3405;
const h0 = 2605.5;
const w1 = 2702.5;
const h1 = 2259.5;

const m = (w0 - w1) / (x0 - x1);
const h = w0 - m * x0;
const n = (h0 - h1) / (z0 - z1);
const g = h0 - n * z0;

const d2_round = (x)=>(Math.round(x*100)/100)

dojo.connect(navigation._map, 'onClick', function (e) {
	var pp = {X:d2_round((((e.mapPoint.x % 10000)-h)/m)),
			  Z:d2_round((((e.mapPoint.y % 10000)-g)/n))};
	console.log(pp);

	var xhttp = new XMLHttpRequest();
	xhttp.open("POST", "https://localhost:8000/");
	xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
	xhttp.send(JSON.stringify({"x": pp["X"], "z": pp["Z"]}));
});

