var data_default = {
  mode: true,
  kondisi: {
    humid_hi: 80,
    humid_lo: 70,
    temp_hi: 33,
    temp_lo: 25,
    soil_hi: 1,
    soil_lo: 0,
    water_hi: 33,
    water_lo: 25
  },
  server_connection: {
    ip: "0.0.0.0",
    port: 5000,
    use_reloader: false,
    debug: false
  }
}


const _comps = {
  id: ['bulletcpu', 'bulletram', 'bullethumid', 'bullettemp', 'bulletair', 'bulletsoil'],
  tinggibullet: innerHeight / 6,
}
for (let bul = 0; bul < _comps.id.length; bul++) {
  $("#bulletsItem").append(
    '<figure class="container p-2 px-0 m-0" id="bull-con"> <div id=' + _comps.id[bul] +
    ' style="height: ' + _comps.tinggibullet + "px" + ';width: 100%;"></div> </figure> '
  )
}

const _tinggibullet = $('#bulletcpu').height(),
  tinggigraph = (_tinggibullet * 4) + 40,
  tinggigauge = (_tinggibullet * 2) - 24,
  lebarbullet = innerWidth / 3

for (let rel = 1; rel < 5; rel++) {
  $("#relays").append(
    '<div class="text-relay">Relay ' + rel + '</div>' +
    '<div class="relay-item">' +
    '<label class="switch"> <input type="checkbox" onchange="Relays.setManual()"' +
    'class="relay" id="relay"> <span class="slider"></span> </label></div>'
  )
}


$("#gauge-item").append(
  '<div class="row gauge-container"> ' +
  ' <div class="col-xl-6 col-sm-6">' +
  '  <div class="card col-12" style="background-color: #2a2a2b">' +
  '   <div class="card-header">Ketinggian Air</div> <div class="card-item"' +
  '   id="gaugeair" style="height: ' + tinggigauge + "px" + ';">' +
  '  </div> </div> </div> ' +
  ' <div class="col-xl-6 col-sm-6">' +
  '  <div class="card col-12" style="background-color: #2a2a2b">' +
  '   <div class="card-header">Kelembapan Air</div> <div class="card-item"' +
  '   id="gaugesoil" style="height: ' + tinggigauge + "px" + ';">' +
  '  </div> </div> </div>' +
  '</div>'
)


$("#myForm").append(
  '<form class="form-container"> <h1>Settings Perkondisian Sensor</h1> <div class="row">' +
  ' <div class="col-3 number"> <label for="humid_hi"><b>Max Humidity</b></label>' +
  ' <input type="number" placeholder="' + data_default.kondisi.humid_hi +
  '"value="' + data_default.kondisi.humid_hi + '" name="humid_hi" required> </div>' +
  ' <div class="col-3 number"> <label for="humid_lo"><b>Min Humidity</b></label>' +
  ' <input type="number" placeholder="' + data_default.kondisi.humid_lo +
  '"value="' + data_default.kondisi.humid_lo + '" name="humid_lo" required> </div>' +
  ' <div class="col-3 number"> <label for="temp_hi"><b>Max Temp</b></label>' +
  ' <input type="number" placeholder="' + data_default.kondisi.temp_hi +
  '"value="' + data_default.kondisi.temp_hi + '" name="temp_hi" required> </div>' +
  ' <div class="col-3 number"> <label for="temp_lo"><b>Min Temp</b></label>' +
  ' <input type="number" placeholder="' + data_default.kondisi.temp_lo +
  '"value="' + data_default.kondisi.temp_lo + '" name="temp_lo" required> </div>' +
  ' <div class="col-3 number"> <label for="water_hi"><b>Max Tinggi Air</b></label>' +
  ' <input type="number" placeholder="' + data_default.kondisi.water_hi +
  '"value="' + data_default.kondisi.water_hi + '" name="water_hi" required> </div>' +
  ' <div class="col-3 number"> <label for="water_lo"><b>Min Tinggi Air</b></label>' +
  ' <input type="number" placeholder="' + data_default.kondisi.water_lo +
  '"value="' + data_default.kondisi.water_lo + '" name="water_lo" required> </div>' +
  ' <div class="col-3"> <label for="use_reloader"><b>Reloader Mode</b></label>' +
  ' <input type="checkbox" placeholder="" name="use_reloader" disabled> </div>' +
  ' <div class="col-3"> <label for="debug"><b>Debug Mode</b></label>' +
  ' <input type="checkbox" placeholder="" name="debug" disabled> </div>' +
  ' </div> <button class="btn" type="button" onclick="data_form.send_change_data(form)">Save Data</button>' +
  ' <button type="button" class="btn cancel" onclick="data_form.closeForm()">Close</button> </form>'
);
