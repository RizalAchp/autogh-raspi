const bulletOptions = {
  chart: {
    inverted: true,
    width:lebarbullet,
    type: 'bullet'
  },
  title: {
    text: null
  },
  legend: {
    enabled: false
  },
  yAxis: {
    gridLineWidth: 0
  },
  plotOptions: {
    series: {
    pointPadding: 0.1,
      borderWidth: 0,
      color: '#000',
      targetOptions: {
        width: '100%'
      }
    }
  },
  credits: {
    enabled: false
  },
  exporting: {
    enabled: false
  }
};
const bulletHumidity = new Highcharts.chart('bullethumid', Highcharts.merge(bulletOptions, {
  chart: {
    marginTop: 40,
  },
  title: {
    text: '2017 YTD'
  },
  yAxis: {
    plotBands: [{
      from: 0,
      to: 150,
      color: '#666'
    }, {
      from: 150,
      to: 225,
      color: '#999'
    }, {
      from: 225,
      to: 9e9,
      color: '#bbb'
    }],
    title: null
  },
  series: [{
    data: [{
      y: 275,
      target: 250
    }]
  }],
  tooltip: {
    pointFormat: '<b>{point.y}</b> (with target at {point.target})'
  }
}));

const bulletTemp = new Highcharts.chart('bullettemp', Highcharts.merge(bulletOptions, {
  chart: {
    marginTop: 40
  },
  title: {
    text: '2017 YTD'
  },
  yAxis: {
    plotBands: [{
      from: 0,
      to: 150,
      color: '#666'
    }, {
      from: 150,
      to: 225,
      color: '#999'
    }, {
      from: 225,
      to: 9e9,
      color: '#bbb'
    }],
    title: null
  },
  series: [{
    data: [{
      y: 275,
      target: 250
    }]
  }],
  tooltip: {
    pointFormat: '<b>{point.y}</b> (with target at {point.target})'
  }
}));

const bulletAir = new Highcharts.chart('bulletair', Highcharts.merge(bulletOptions, {
  chart: {
    marginTop: 40
  },
  title: {
    text: '2017 YTD'
  },
  yAxis: {
    plotBands: [{
      from: 0,
      to: 150,
      color: '#666'
    }, {
      from: 150,
      to: 225,
      color: '#999'
    }, {
      from: 225,
      to: 9e9,
      color: '#bbb'
    }],
    title: null
  },
  series: [{
    data: [{
      y: 275,
      target: 250
    }]
  }],
  tooltip: {
    pointFormat: '<b>{point.y}</b> (with target at {point.target})'
  }
}));

const bulletCpu = new Highcharts.chart('bulletcpu', Highcharts.merge(bulletOptions, {
  chart: {
    marginTop: 40
  },
  title: {
    text: '2017 YTD'
  },
  yAxis: {
    plotBands: [{
      from: 0,
      to: 150,
      color: '#666'
    }, {
      from: 150,
      to: 225,
      color: '#999'
    }, {
      from: 225,
      to: 9e9,
      color: '#bbb'
    }],
    title: null
  },
  series: [{
    data: [{
      y: 275,
      target: 250
    }]
  }],
  tooltip: {
    pointFormat: '<b>{point.y}</b> (with target at {point.target})'
  }
}));
const bulletRam = new Highcharts.chart('bulletram', Highcharts.merge(bulletOptions, {
  chart: {
    marginTop: 40
  },
  title: {
    text: '2017 YTD'
  },
  yAxis: {
    plotBands: [{
      from: 0,
      to: 150,
      color: '#666'
    }, {
      from: 150,
      to: 225,
      color: '#999'
    }, {
      from: 225,
      to: 9e9,
      color: '#bbb'
    }],
    title: null
  },
  series: [{
    data: [{
      y: 275,
      target: 250
    }]
  }],
  tooltip: {
    pointFormat: '<b>{point.y}</b> (with target at {point.target})'
  }
}));
const bulletDisk = new Highcharts.chart('bulletdisk', Highcharts.merge(bulletOptions, {
  chart: {
    marginTop: 40
  },
  title: {
    text: '2017 YTD'
  },
  yAxis: {
    plotBands: [{
      from: 0,
      to: 150,
      color: '#666'
    }, {
      from: 150,
      to: 225,
      color: '#999'
    }, {
      from: 225,
      to: 9e9,
      color: '#bbb'
    }],
    title: null
  },
  series: [{
    data: [{
      y: 275,
      target: 250
    }]
  }],
  tooltip: {
    pointFormat: '<b>{point.y}</b> (with target at {point.target})'
  }
}));
const gaugeOptions = {
  chart: {type: 'solidgauge'},
  title: null,
  pane: {
    center: ['50%', '80%'],
    size: '100%',
    startAngle: -90,
    endAngle: 90,
    background: {
      innerRadius: '60%',
      outerRadius: '100%',
      shape: 'arc'
    }
  },

  exporting: {
    enabled: false
  },

  tooltip: {
    enabled: false
  },

  yAxis: {
    stops: [
      [0.1, '#55BF3B'],
      [0.5, '#DDDF0D'],
      [0.9, '#DF5353']
    ],
    lineWidth: 0,
    tickWidth: 0,
    minorTickInterval: null,
    tickAmount: 2,
    labels: {
      y: 20
    }
  },

  plotOptions: {
    solidgauge: {
      dataLabels: {
        size: "100%",
        borderWidth: 0,
        useHTML: true
      }
    }
  }
};

var chartAir = Highcharts.chart('gaugeair', Highcharts.merge(gaugeOptions, {
  yAxis: {
    min: 0,
    max: 200,
  },

  credits: {
    enabled: false
  },

  series: [{
    name: 'Tinggi Air',
    data: [80],
    dataLabels: {
      format:
        '<div class="data-label-gauge d-flex flex-column">' +
        '<span class="header-gauge">{y}</span>' +
        '<span class="text-gauge">percent(%)</span>' +
        '</div>'
    },
    tooltip: {
      valueSuffix: ' %'
    }
  }]

}));
var chartSoil = Highcharts.chart('gaugesoil', Highcharts.merge(gaugeOptions, {
  yAxis: {
    min: 0,
    max: 200,
  },

  credits: {
    enabled: false
  },

  series: [{
    name: 'Kelembapan Tanah',
    data: [80],
    dataLabels: {
      format:
        '<div class="data-label-gauge d-flex flex-column">' +
        '<span class="header-gauge" >{y}</span>' +
        '<span class="text-gauge" >percent (%)</span>' +
        '</div>'
    },
    tooltip: {
      valueSuffix: ' %'
    }
  }]

}));

const colors = Highcharts.getOptions().colors;

Highcharts.setOptions({chart: {style: {fontFamily: "Ubuntu", }, }, });
const chartOne = new Highcharts.chart({
  chart: {
    renderTo: "charthumidsuhu",
    type: "spline",
    height: tinggigraph + "px",
  },
  legend: {symbolWidth: 100},
  time: {useUTC: false},
  line: {animation: false, dataLabels: {enabled: true}},
  title: {text: "Humidity dan Temperature", style: {"fontSize": "14px"}},

  subtitle: {text: "Humidity (%) & Temperature (C)", style: {"fontSize": "10px"}},
  exporting: {enabled: true},
  xAxis: {
    title: {
      text: "Time",
    },
    accessibility: {description: "Interval waktu Menit:Detik"},
    tickInverval: 150,
    ordinal: false,
  },

  plotOptions: {series: {cursor: "pointer"}},
  yAxis: {softMin: 0, softMax: 30},
  credits: {enabled: false},
  series: [
    {
      name: "Humidity",
      data: [],
      dashStyle: "ShortDot",
      color: colors[5],
      tooltip: {valueSuffix: " % (persen)"},
    },
    {
      name: "Suhu",
      data: [],
      dashStyle: "ShortDash",
      color: colors[1],
      tooltip: {valueSuffix: " C"},
    },
  ],

  responsive: {
    rules: [
      {
        condition: {maxWidth: 550},
        chartOptions: {
          chart: {spacingLeft: 3, spacingRight: 3},
          legend: {itemWidth: 250},
          xAxis: {title: "Timer Interval"},
          yAxis: {visible: true},
        },
      },
    ],
  },
});


// Bring life to the dials
const intervalgauge = setInterval(function () {
  // Speed
  var point,
    newVal,
    inc;

  if (chartSpeed) {
    point = chartSpeed.series[0].points[0];
    inc = Math.round((Math.random() - 0.5) * 100);
    newVal = point.y + inc;

    if (newVal < 0 || newVal > 200) {
      newVal = point.y - inc;
    }

    point.update(newVal);
  }

  // RPM
  if (chartRpm) {
    point = chartRpm.series[0].points[0];
    inc = Math.random() - 0.5;
    newVal = point.y + inc;

    if (newVal < 0 || newVal > 5) {
      newVal = point.y - inc;
    }

    point.update(newVal);
  }
}, 2000);

clearInterval(intervalgauge)
