var sockio = null,
  selected_port;
const categories = [],
  LocIP = location.protocol + "//" + document.domain + ":" + location.port;

const callback_data = (msg) => {
  const date = new Date().getTime()
  Datas.value_gauges(msg)
  Datas.value_charts(msg, date)
  Datas.value_bullets(msg)
}
const Datas = {
  value_gauges: (data) => {
    const point = [chartAir.series[0].points[0], chartSoil.series[0].points[0]];
    point[0].update(data.tinggiair)
    point[1].update(data.soil)
  },
  value_charts: (data, tgl) => {
    const terus = chartOne.series[0].length >= 100 ? true : false
    chartOne.series[0].addPoint([tgl, data], true, terus, true)
    chartOne.series[2].addPoint([tgl, data], true, terus, true)
  },
  value_bullets: (data) => {
    bulletHumidity.series[0].points[0].update(data.humid)
    bulletTemp.series[0].points[0].update(data.temp)
    bulletAir.series[0].points[0].update(data.tinggiair)
    bulletCpu.series[0].points[0].update(data.cpu)
    bulletRam.series[0].points[0].update(data.ram)
  },
  send_data: (evnt, data) => {
    if (data) {
      sockio.emit(evnt, data);
    } else {
      sockio.emit(evnt);
    }
  },
  log: (txt) => {
    const newLine = document.createElement("li"),
      consoles = document.querySelector('#console'),
      lines = $('li')

    newLine.innerHTML = (typeof txt === 'string') ? txt : JSON.stringify(txt, null, 4);
    if (lines.length > 5) {
      consoles.removeChild(consoles.firstElementChild)

    }
    consoles.appendChild(newLine);
  }
};
const Relays = {
  modget: document.getElementById("relmode"),
  get: document.querySelectorAll("input[type=checkbox]#relay"),
  mode: () => {
    return Relays.modget.checked ? "auto" : "manual";
  },
  setManual: () => {
    const kondisi = [];
    for (let i = 0; i < Relays.get.length; i++) {
      kondisi.push(Relays.get[i].checked);
    }
    return Datas.send_data("onrelaychange", {value: kondisi});
  },
  set: (kond) => {
    let k = 0;
    const kondisi = [];
    for (; k < Relays.kondisi.length; k++) {
      Relays.get[k].checked = kond ? kond[k] : Relays.kondisi[k];
      kondisi.push(Relays.get[k].checked);
    }
    return kondisi;
  },
  change: (comp) => {
    const status = $("#status_mode");
    if (comp?.checked) {
      // MODE AUTO
      Datas.send_data("modeauto", null);
      status.text("MODE AUTO (Close Loop)");
      Relays.get.forEach((element) => (element.disabled = true));
      comp.disabled = false;
      loading.do()
    } else {
      // MODE MANUAL
      Datas.send_data("modemanual", null);
      status.text("MODE MANUAL (Open Loop)");
      Relays.get.forEach(
        (element) => ((element.disabled = false), (element.checked = false))
      );
      Relays.kondisi = [false, false, false, false];
    }
  },
};

$(document).ready(() => {
  sockio = io();
  sockio.connect(LocIP);

  sockio.on("data_sensor", Datas.callback_data);

  sockio.on("relay_feedback", (msg) => {
    console.log(msg?.msg.value);
  });

  sockio.on("mode", (msg) => {
    console.log(msg?.value);
  });

  sockio.on("status", (msg) => {
    console.log(msg?.sts);
  });

  sockio.on("restart", (msg) => {
    console.log(msg?.sts);
  });
  Relays.modget.checked = true;
  Relays.change(Relays.modget);
});

const data_form = {
  get_data: () => {
    return $("form")
      .serializeArray()
      .reduce((obj, item) => {
        obj[item.name] = Number(item.value);
        return obj;
      }, {});
  },
  change_data: () => {},
  openForm: () => {
    document.getElementById("myForm").style.display = "block";
  },
  closeForm: () => {
    document.getElementById("myForm").style.display = "none";
  },
};

class Image {
  constructor(imgUrl, size) {
    this.imgUrl = imgUrl;
    this.size = size;
  }
  backgroundImage() {
    // console.log("inside function ");
    var img = document.querySelector(".isloading");
    var text =
      "margin:auto;" +
      "background-image: url(" +
      this.imgUrl +
      ");" +
      "background-size:auto;" +
      "opacity:0.6;" +
      "background-blend-mode: darken;" +
      "height: " +
      this.size +
      "vh;" +
      "z-index: 1;" +
      "position: fixed;";
    img.style.cssText = text;
  }
}
const loading = {
  do: () => {
    var img = document.querySelector(".isloading");
    const obj = new Image("static/img/animation.gif", 100);
    obj.backgroundImage();
    setTimeout(() => {img.remove()}, 2000)
  },
};

const sidebar_item = {
  showLog: (text, desc) => {},
};
