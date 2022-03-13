const colors = Highcharts.getOptions().colors;
Highcharts.setOptions({chart: {style: {fontFamily: "Ubuntu", }, }, });
const bulletOptions = {
  chart: {inverted: true, width: lebarbullet, type: 'bullet'},
  title: {text: null},
  legend: {enabled: false},
  yAxis: {gridLineWidth: 0},
  plotOptions: {
    series: {
      pointPadding: 0.1, borderWidth: 0,
      targetOptions: {minWidth: '10%'}
    }
  }, credits: {
    enabled: false
  }, exporting: {enabled: false}
};

const Bullets = {

  bulletHumid: new Highcharts.chart('bullethumid', Highcharts.merge(bulletOptions, {
    chart: {marginTop: 20, },
    title: {text: 'Humidity DHT11', style: {"fontSize": "14px"}},
    yAxis: {
      plotBands: [{
        from: 0, to: 30, color: '#666'
      }, {
        from: 30, to: 60, color: '#999'
      }, {
        from: 60, to: 100, color: '#bbb'
      }], title: null
    },
    series: [{
      data: [{y: 36, target: 90}],
      color: colors[5]
    }], tooltip: {pointFormat: '<b>{point.y} %</b> (Max Humidity Ruangan {point.target} %)'}
  })),

  bulletTemp: new Highcharts.chart('bullettemp', Highcharts.merge(bulletOptions, {
    chart: {marginTop: 20},
    title: {text: 'Temperature DHT11', style: {"fontSize": "14px"}},
    yAxis: {
      plotBands: [{
        from: 0, to: 20.0, color: '#666'
      }, {
        from: 20.0, to: 40.0, color: '#999'
      }, {
        from: 50.0, to: 9e9, color: '#bbb'
      }], title: null
    }, series: [{
      data: [{y: 10.0, target: 40.0}],
      color: colors[1]
    }], tooltip: {pointFormat: '<b>{point.y} C</b> (Max Suhu Rangan {point.target} C)'}
  })),

  bulletAir: new Highcharts.chart('bulletair', Highcharts.merge(bulletOptions, {
    chart: {marginTop: 20},
    title: {text: 'Tinggi Air HCSR04', style: {"fontSize": "14px"}},
    yAxis: {
      plotBands: [{
        from: 0, to: 30, color: '#666'
      }, {
        from: 30, to: 60, color: '#999'
      }, {
        from: 60, to: 120, color: '#bbb'
      }], title: null
    }, series: [{
      data: [{y: 1, target: 120}], color: colors[7]
    }],
    tooltip: {pointFormat: '<b>{point.y} cm</b> (Max Ketinggian Air {point.target} cm)'}
  })),

  bulletCpu: new Highcharts.chart('bulletcpu', Highcharts.merge(bulletOptions, {
    chart: {marginTop: 20},
    title: {text: 'RESOURCE CPU', style: {"fontSize": "14px"}},
    yAxis: {
      plotBands: [{
        from: 0, to: 35, color: '#666'
      }, {
        from: 35, to: 70, color: '#999'
      }, {
        from: 70, to: 9e9, color: '#bbb'
      }], title: null
    }, series: [{
      data: [{y: 1, target: 80}],
      color: colors[2]
    }], tooltip: {pointFormat: '<b>{point.y} %</b> (Max Uage CPU {point.target} %)'}
  })),
  bulletRam: new Highcharts.chart('bulletram', Highcharts.merge(bulletOptions, {
    chart: {marginTop: 20},
    title: {text: 'RESOURCE RAM', style: {"fontSize": "14px"}},
    yAxis: {
      plotBands: [{
        from: 0, to: 1000, color: '#666'
      }, {
        from: 1000, to: 1500, color: '#999'
      }, {
        from: 1500, to: 2e90, color: '#bbb'
      }], title: null
    }, series: [{
      data: [{y: 500, target: 1800}],
      color: colors[3]
    }], tooltip: {
      pointFormat: '<b>{point.y} KB</b> (Max Usage RAM {point.target} KB)'
    }
  })),
  bulletSoil: new Highcharts.chart('bulletsoil', Highcharts.merge(bulletOptions, {
    chart: {marginTop: 20},
    title: {text: 'Kelembapan Tanah', style: {"fontSize": "14px"}},
    yAxis: {
      plotBands: [{
        from: 0, to: 150, color: '#666'
      }, {
        from: 150, to: 225, color: '#999'
      }, {
        from: 225, to: 9e9, color: '#bbb'
      }], title: null
    }, series: [{
      data: [{y: 10, target: 89}],
      color: colors[4]
    }]
  }))
}

const gaugeOptions = {
  chart: {type: 'solidgauge'}, title: null,
  pane: {
    center: ['50%', '80%'], size: '100%', startAngle: -90, endAngle: 90,
    background: {
      innerRadius: '60%', outerRadius: '100%', shape: 'arc'
    }
  },
  exporting: {enabled: false},
  tooltip: {enabled: false},
  yAxis: {
    stops: [[0.1, '#55BF3B'], [0.5, '#DDDF0D'], [0.9, '#DF5353']],
    lineWidth: 0, tickWidth: 0,
    minorTickInterval: null,
    tickAmount: 2, labels: {y: 20}
  },
  plotOptions: {
    solidgauge: {dataLabels: {size: "100%", borderWidth: 0, useHTML: true}}
  }
};

const Gauges = {

  chartAir: Highcharts.chart('gaugeair', Highcharts.merge(gaugeOptions, {
    yAxis: {
      min: 0,
      max: 150,
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

  })),
  chartSoil: Highcharts.chart('gaugesoil', Highcharts.merge(gaugeOptions, {
    yAxis: {
      min: 0,
      max: 100,
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

  }))
};

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
    type: "datetime",
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

