import urllib.request
import json
import os
import re

KEYS = ['iPad', 'iPhone', 'Android', 'Windows']
URL = 'http://firefire.cyber.org.il/logs/access_130101.zip'
HTML = "canvasjs-3/my.html"
PARENT = "http://firefire.cyber.org.il/logs/"
CODE = 'unicode_escape'
PATTERN = "access_[0-9]+.zip"

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


def get_dict(keys):
    return {k: 0 for k in keys}


def parse_file(url_path, plat_dict, counter):
    print(url_path)
    with urllib.request.urlopen(url_path) as f:
        lines = f.readlines()
    if not lines:
        return counter
    counter += len(lines)
    for line in lines:
        line_s = str(line)
        for k in plat_dict:
            if k in line_s:
                plat_dict[k] += 1
                continue
    return counter


def get_final_dict(plat_dict, counter):
    for k in plat_dict:
        plat_dict[k] /= counter
        plat_dict[k] = round(plat_dict[k] * 100, 2)
    return plat_dict


def print_percents(plat_dict):
    for k in plat_dict:
        print(f"{k} - {plat_dict[k]}%")
    return plat_dict


def write_html(plat_dict, path):
    with open(path, "w") as f:
        f.write(PART_1 + '\n')
        for k in plat_dict:
            f.write('{ ')
            f.write(f'y: {plat_dict[k]}, label: "{k}"')
            f.write('},\n')
        f.write(PART_2)


def run_html():
    os.system(f"open {HTML}")


def write_json(plat_dict):
    with open("my.json", "w") as f:
        f.write(json.dumps(plat_dict))


def parse_all_files(parent):
    counter = 0
    plat_dict = get_dict(KEYS)
    with urllib.request.urlopen(parent) as f:
        lines = f.readlines()
        for line in lines:
            s = re.search(PATTERN, str(line))
            if s:
                counter = parse_file(PARENT + s.group(), plat_dict, counter)
                print(counter)
                print(plat_dict)
    plat_dict = get_final_dict(plat_dict, counter)
    write_html(plat_dict, HTML)
    run_html()


if __name__ == '__main__':
    parse_all_files(PARENT)
