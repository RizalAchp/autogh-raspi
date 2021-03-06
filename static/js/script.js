var sockio = null,
  selected_port;
const categories = [],
  LocIP = location.protocol + "//" + document.domain + ":" + location.port;

const callback_data = (msg) => {
  const date = new Date().getTime();
  Datas.change_values(msg, date);
};


const Datas = {
  change_values: (data, tgl) => {
    const point = [
      Gauges.chartAir.series[0].points[0],
      Gauges.chartSoil.series[0].points[0],
    ],
      terus = chartOne.series[0].length >= 100 ? true : false;

    console.log(typeof data.temps)
    point[0].update(data.tinggiair);
    point[1].update(data.soil);
    chartOne.series[0].addPoint([tgl, data.humid], true, terus, true);
    chartOne.series[1].addPoint([tgl, data.temps], true, terus, true);
    Bullets.bulletHumid.series[0].points[0].update(data.humid);
    Bullets.bulletTemp.series[0].points[0].update(data.temps);
    Bullets.bulletSoil.series[0].points[0].update(data.soil);
    Bullets.bulletAir.series[0].points[0].update(data.tinggiair);
  },

  value_resource: (data) => {
    Bullets.bulletCpu.series[0].points[0].update(data.cpu);
    Bullets.bulletRam.series[0].points[0].update(data.ram);
  },
  send_data: (evnt, data) => {
    const withdata = () => {
      sockio.emit(evnt, data);
    },
      withoutdata = () => {
        sockio.emit(evnt);
      };
    return data ? withdata() : withoutdata();
  },
  log: (txt) => {
    const newLine = document.createElement("li");

    newLine.innerHTML =
      typeof txt === "string" ? txt : JSON.stringify(txt, null, 4);

    const removes = () => {
      consoles.removeChild(
        document.querySelector("#console").firstElementChild
      );
    },
      add = () => {
        consoles.appendChild(newLine);
      };

    if (lines.length > 5) {removes();}
    return add();
  },
};


const Relays = {
  modget: document.getElementById("relmode"),
  get: document.querySelectorAll("input[type=checkbox]#relay"),
  setManual: () => {
    const kondisi = [];
    for (let i = 0; i < Relays.get.length; i++) {
      kondisi.push(Relays.get[i].checked);
    }
    return Datas.send_data("onrelaychange", {value: kondisi});
  },
  set: (konds) => {
    let k = 0;
    kond = konds.value
    const kondisi = [];
    for (; k < Relays.get.length; k++) {
      Relays.get[k].checked = kond[k] ? true : false;
      kondisi.push(Relays.get[k].checked);
    }
    return kondisi;
  },
  change: () => {
    const status = $("#status_mode");
    if (Relays.modget.checked) {
      // MODE AUTO
      Datas.send_data("modeauto");
      status.text("MODE AUTO (Close Loop)");
      Relays.get.forEach((element) => (element.disabled = true, element.checked = false));
      Relays.modget.disabled = false;
      loading.do(1);
    } else {
      // MODE MANUAL
      Datas.send_data("modemanual", {value: [false, false, false, false]});
      status.text("MODE MANUAL (Open Loop)");
      Relays.get.forEach((element) => (element.disabled = false, element.checked = false));
    }
  },
};

const data_form = {
  get_data: () => {
    return $("form")
      .serializeArray()
      .reduce((obj, item) => {
        obj[item.name] = Number(item.value);
        return obj;
      }, {});
  },
  send_change_data: () => {
    Datas.send_data('setting_change', data_form.get_data());
  },
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
    const node = $(".isloading")[0],
      text =
        "margin:auto;" + "background-image: url(" + this.imgUrl + ");" +
        "background-size:100%;" + "opacity:0.6;" + "background-blend-mode: darken;" +
        "height: " + this.size + "vh;" + "position: absolute;" + "z-index: 9;";
    node.style.cssText = text;
  }
}
const loading = {
  do: (delay) => {
    $("body").prepend('<div class="isloading"></div>');
    let obj = new Image("static/img/animation.gif", innerHeight);
    obj.backgroundImage();

    setTimeout(() => {
      $(".isloading").remove();
    }, delay * 1000);
  },
};

$(document).ready(() => {
  sockio = io();
  sockio.connect(LocIP);

  sockio.on("data_sensor", callback_data);
  sockio.on("resource", Datas.value_resource)
  sockio.on("relay_feedback", Relays.set)

  sockio.on("mode", (msg) => {
    Relays.modget.checked = msg?.value;
    Relays.change();
  });

  sockio.on("status", (msg) => {
    console.log(msg?.sts);
    console.log(msg?.msg);
  });

  sockio.on("restart", (msg) => {
    console.log(msg?.sts);
  });

  setInterval(() => {
    sockio.emit("get_resource");
  }, 10 * 1000)
});
