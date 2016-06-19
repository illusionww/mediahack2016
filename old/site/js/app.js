$(document).ready(function () {
    init_graph();
});

function init_graph() {
    var $graph = $("#graph");
    var cw = $graph.width();
    $graph.css({'height':cw/2.5+'px'});

    var margin = {top: 20, right: 150, bottom: 30, left: 50};
    var width = $graph.width() - margin.left - margin.right;
    var height = $graph.height() - margin.top - margin.bottom;

    var parseDate = d3.time.format("%Y%m%d").parse;

    var x = d3.time.scale()
        .range([0, width]);

    var y1 = d3.scale.linear()
        .range([height, 0]);

    var color = d3.scale.category10();

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y1)
        .orient("left");

    var line = d3.svg.line()
        .interpolate("basis")
        .x(function (d) {
            return x(d.date);
        })
        .y(function (d) {
            return y1(d.y_values);
        });

    var svg = d3.select("#graph").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    d3.tsv("dynamic.tsv", function (error, data) {
        if (error) throw error;

        color.domain(d3.keys(data[0]).filter(function (key) {
            return key !== "date";
        }));

        data.forEach(function (d) {
            d.date = parseDate(d.date);
        });

        var curves = color.domain().map(function (name) {
            return {
                name: name,
                values: data.map(function (d) {
                    return {date: d.date, y_values: +d[name]};
                })
            };
        });

        x.domain(d3.extent(data, function (d) {
            return d.date;
        }));

        y1.domain([
            d3.min(curves, function (c) {
                return d3.min(c.values, function (v) {
                    return v.y_values;
                });
            }),
            d3.max(curves, function (c) {
                return 90
            })
        ]);

        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);

        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)
            .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", ".71em")
            .style("text-anchor", "end");

        var curve = svg.selectAll(".curve")
            .data(curves)
            .enter().append("g")
            .attr("class", "curve");

        curve.append("path")
            .attr("class", "line")
            .attr("d", function (d) {
                return line(d.values);
            })
            .style("stroke", function (d) {
                return color(d.name);
            });

        curve.append("text")
            .datum(function (d) {
                return {name: d.name, value: d.values[d.values.length - 1]};
            })
            .attr("transform", function (d) {
                return "translate(" + x(d.value.date) + "," + y1(d.value.y_values) + ")";
            })
            .attr("x", 3)
            .attr("dy", ".35em")
            .text(function (d) {
                return d.name;
            });

        //add_vertical_line("11.11.2011", "Рубль упал и вся жизнь переменилась!");
        //add_vertical_line("12.04.2012", "Ну теперь точно конец!");
        //add_vertical_line("12.08.2012", "Всё.....");

        initCircles1();

    });

    function add_vertical_line(date, text) {
        // Add vertical line
        var x_value = x(parseDate(date));
        svg.append("line")
            .attr({
                x1: x_value,
                x2: x_value,
                y1: height,
                y2: 20
            })
            .attr("class", "eventLine");

        svg.append("text")
            .attr("class", "eventText")
            .attr("x", x_value)
            .attr("y", 20 - 10)
            .attr("text-anchor", "start")
            .text(text);
    }

    function initCircles1() {
        var parseDate = d3.time.format("%d.%m.%Y").parse;


        d3.tsv("euro.tsv", function (error, data) {
            if (error) throw error;

            data.forEach(function (d) {
                d["date"] = parseDate(d["date"]);
            });

            var yScale = d3.scale.linear()
                .domain([0, 20000])
                .range([height, 0]);

            var yAxis = d3.svg.axis()
                .scale(yScale)
                .orient("right");

            svg.append("g")
                .attr("class", "y axis")
                .call(yAxis)
                .append("text")
                .attr("transform", "rotate(-90)")
                .attr("y", 6)
                .attr("dy", ".71em")
                .style("text-anchor", "end");


            svg.selectAll("circle.one")
                .data(data)
                .enter()
                .append("circle")
                .attr("cx", function(d) {
                    return x(d["date"]);
                })
                .attr("cy", function(d) {
                    return yScale(d["smi_count"]);
                })
                .attr("r", function(d) {
                    return 5;
                })
                .attr("fill", "rgba(31, 119, 180, 0.5)");

            initCircles2();
        })
    }

    function initCircles2() {
        var parseDate = d3.time.format("%d.%m.%Y").parse;


        d3.tsv("dollar.tsv", function (error, data) {
            if (error) throw error;

            data.forEach(function (d) {
                d["date"] = parseDate(d["date"]);
            });

            var yScale = d3.scale.linear()
                .domain([0, 20000])
                .range([height, 0]);

            svg.selectAll("circle.two")
                .data(data)
                .enter()
                .append("circle")
                .attr("cx", function(d) {
                    return x(d["date"]);
                })
                .attr("cy", function(d) {
                    return yScale(d["smi_count"]);
                })
                .attr("r", function(d) {
                    return 5;
                })
                .attr("fill", "rgba(255, 127, 14, 0.5)");

            svg.select ("text")
                .data([])
                .text(function (d) {
                    return d.name;
                });
        })
    }
}

