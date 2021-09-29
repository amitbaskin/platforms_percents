import urllib.request
import json

KEYS = ['iPad', 'iPhone', 'Android', 'Windows']
URL = 'http://firefire.cyber.org.il/logs/access_130101.zip'

PART_1 = """
<!DOCTYPE HTML>
<html lang="">
<head>
<script>
window.onload = function() {

var chart = new CanvasJS.Chart("chartContainer", {
	theme: "light2", // "light1", "light2", "dark1", "dark2"
	exportEnabled: true,
	animationEnabled: true,
	title: {
		text: "Platforms Percentages"
	},
	data: [{
		type: "pie",
		startAngle: 25,
		toolTipContent: "<b>{label}</b>: {y}%",
		showInLegend: "true",
		legendText: "{label}",
		indexLabelFontSize: 16,
		indexLabel: "{label} - {y}%",
		dataPoints: [
"""

PART_2 = """
]
	}]
});
chart.render();

}
</script>
    <title></title>
</head>
<body>
<div id="chartContainer" style="height: 370px; width: 100%;"></div>
<script src="https://canvasjs.com/assets/script/canvasjs.min.js"></script>
</body>
</html>
"""


def get_lines(url_path):
    with urllib.request.urlopen(url_path) as f:
        return f.readlines()


def get_dict(keys):
    return {k: 0 for k in keys}


def parse_file(lines, plat_dict):
    for line in lines:
        line_s = line.decode('unicode_escape')
        for k in plat_dict:
            if k in line_s:
                plat_dict[k] += 1
                continue
    for k in plat_dict:
        plat_dict[k] /= len(lines)
        plat_dict[k] = round(plat_dict[k] * 100, 2)


def get_percents(keys, url):
    plat_dict = get_dict(keys)
    lines = get_lines(url)
    parse_file(lines, plat_dict)
    return plat_dict


def print_percent(plat_dict):
    for k in plat_dict:
        print(f"{k} - {plat_dict[k]}%")
    return plat_dict


def write_html(plat_dict):
    with open("canvasjs-3/my.html", "w") as f:
        f.write(PART_1 + '\n')
        for k in plat_dict:
            f.write('{ ')
            f.write(f'y: {plat_dict[k]}, label: "{k}"')
            f.write('},\n')
        f.write(PART_2)


if __name__ == '__main__':
    write_html(get_percents(KEYS, URL))
