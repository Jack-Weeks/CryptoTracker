from datetime import datetime

bgd_col='#192D4B'
big_tile_col='#132238'
small_tile_col = '#1F395E'

def get_color(value):
    print(value, type(value))
    if type(value) == float:
        print(str(value))
        if str(value)[0] == '-':
            return '#B93535'
        elif value == 0.00:
            return "#4E4E50"
        else:
            return '#358F5D'
    else:

        value2 = float(value[:-2])
        if value2 > 0:
            return '#358F5D'
        elif value2 == 0.00:
            return "#4E4E50"
        else:
            return '#B93535'



def make_html(data, path):
    with open(path, 'w') as openfile:
        openfile.write(f"""
            <!doctype html>
    <html lang="en" style="background-color:{bgd_col}">
      <head style="background-color:{bgd_col}">
        <title>{datetime.now().strftime("%d/%m/%Y %H:%M")}</title>"""
        """<!-- Required meta tags -->
        <meta charset="utf-8">
        <meta content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0" name="viewport" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
        <!--  Fonts and icons  -->
          <!--     Fonts and icons     -->
    <link href="https://fonts.googleapis.com/css?family=Poppins:200,300,400,600,700,800" rel="stylesheet">
    <link href="https://use.fontawesome.com/releases/v5.0.6/css/all.css" rel="stylesheet">

        <!-- Black Dashboard CSS -->
        <link href="assets/css/black-dashboard.css?v=1.0.0" rel="stylesheet" />
        <style>
            .card{
        border-radius: 4px;

        box-shadow: 0 6px 10px rgba(0,0,0,.08), 0 0 6px rgba(0,0,0,.05);
          transition: .3s transform cubic-bezier(.155,1.105,.295,1.12),.3s box-shadow,.3s -webkit-transform cubic-bezier(.155,1.105,.295,1.12);

      cursor: pointer;
    }

    .card:hover{
         transform: scale(1.01);
      box-shadow: 0 10px 20px rgba(0,0,0,.12), 0 4px 8px rgba(0,0,0,.06);}
        </style>
      </head>
      <body>"""
       +
                       f"""
    <div class="container-fluid" style="background-color:{bgd_col}">
      <div class="container-fluid" style="margin-top: 5%">

        <div class="content">
          <div class="container-fluid">
              <div class="row">
              <div class="col col-lg-6">
                <div class="card card-chart" style="background-color: {small_tile_col};">
                  <div class="card-header ">
                    <div class="row">
                      <div class="col-sm-6 text-left">
                        <h6 class="card-subtitle text-muted" style="padding:2%">Total gains</h6>
                        <h2 class="card-title" style="font-size:32px"><strong>${data['Totals']['Total']} <span style='color:{get_color(data['Totals']["Today's Gain $"])};font-size:22px'>${data['Totals']["Today's Gain $"]}</span></strong></h2>
                      </div>
                    </div>
                  </div>
                  <div class="card-body" style="width:100%;margin: 0px;padding: 0px">
                    <div class="chart-area" style="width:100%">
                      <canvas id="canvas-total">

                      </canvas>
                    </div>
                  </div>
                </div>
              </div>
            
            
              <div class="col col-lg-6">
                <div class="card card-chart" style="background-color: {small_tile_col};">
                  <div class="card-header ">
                    <div class="row">
                      <div class="col-sm-6 text-left">
                        <h6 class="card-subtitle text-muted" style="padding:2%">Daily gains</h6>
                        <h2 class="card-title" style="font-size:32px"><strong>${data['Totals']["Today's Gain $"]}</strong></h2>
                      </div>
                    </div>
                  </div>
                  <div class="card-body" style="width:100%;margin: 0px;padding: 0px">
                    <div class="chart-area">
                      <canvas id="canvas-daily">

                      </canvas>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            """)

        openfile.write(f"""
                      <div class="row">
                  <div class="col-12">
                      <div class="card" style="background-color: {big_tile_col}">
                          <div class="card-body">
                              <div class="row">
                                  <div class="col">
                                      <div class="row">
        """)
        for item in data.keys():
            if item != 'Totals':
                openfile.write(f"""
                                            <div class="col-xl-2 col-lg-3 col-md-4 col-6">
                                                              <div class="card" style="background-color:{small_tile_col};height:10rem">
                                                      <div class="card-header" style="margin-top: 2%;">
                                                          <h6 class="card-subtitle" style="font-size: 22px">{item}</h6>
                                                      </div>
                                                      <div class="card-body" style="text-align: right">
                                                          <h4 class="card-title" style="font-size:24px"><strong>{data[item]['Current Balance'].split()[0]} <span style="color:{get_color(data[item]['Daily % Change'])};font-size:18px;font-weight:600">{data[item]['Daily % Change']}</span></strong></h4>
                                                          <h6 class="card-subtitle mb-2 text-muted" style="font-size: 16px">{data[item]['Current Value']}</h6>
                                                      </div>
                                                  </div>
                                              </div>
                """)
        openfile.write("""
                                              </div>
                                  </div>
                              </div>
                          </div>
                      </div>
                  </div>
              </div>
        """)


        for item in data.keys():
            if item != 'Totals':
                openfile.write(f"""
                    <div class="card" style="padding: 3%;background-color: {big_tile_col};">
                              <div class="row">
                      <div class="col-12">

                          <h4 class="title" style="font-size:30px">{item}</h4>
                      </div>
                      <div class="col-sm-12 col-md-6 col-lg-6 col-xl-6">
                                  <div class="card" style="background-color: {small_tile_col};">
                                                                <div class="card-header">
                                        <h4 class="card-title" style="font-size:24px"><strong>{data[item]['Current Balance']} <span style="color:{get_color(data[item]['Daily % Change'])};font-size:18px">{data[item]['Daily % Change']}</span><span class="card-subtitle mb-2 text-muted" style="font-size:18px;text-align:right"> / {data[item]['Current Value']}</span></strong></h4>
                                        <h6 class="card-subtitle mb-2 text-muted">Total</h6>
                              </div>
                                      <div class="card-body" style="width:100%;margin: 0px;padding: 0px">
                                          <div class="chart-area">
                                              <canvas id="canvas-{item}">
                                              </canvas>
                                            </div>
                                      </div>
                                  </div>
                      </div>
                      <div class=" col-sm-12 col-md-6 col-lg-6 col-xl-6">
                        <div class="row">
                    """)
                for i in data[item].keys():
                    if (item == 'XCH' or item == 'AR') and (i == 'Current Price'):
                        openfile.write(f"""
                                  <div class="col-6 col-xl-6">
                                      <div class="card" style="height:8rem;background-color: {small_tile_col};">
                                          <div class="card-body">
                                            <h4 class="card-title" style="font-size:24px"><strong>{data[item][i]} <span style="color:{get_color(data[item]['24hr Price Change %'])};font-size:18px">{data[item]['24hr Price Change %']}</span></strong></h4>
                                            <h6 class="card-subtitle mb-2 text-muted">{i}</h6>
                                          </div>
                                    </div>
                                  </div>

                            """)
                    elif i == 'Average Daily Increase':
                        openfile.write(f"""
                                  <div class="col-6 col-xl-6">
                                      <div class="card" style="height:8rem;background-color: {small_tile_col};">
                                          <div class="card-body">
                                            <h4 class="card-title" style="font-size:24px"><strong>{data[item][i]}<span class="card-subtitle mb-2 text-muted" style="font-size:18px;text-align:right"> / {data[item]['Average Daily Value Increase']}</span></strong></h4>
                                            <h6 class="card-subtitle mb-2 text-muted">{i}</h6>
                                          </div>
                                    </div>
                                  </div>

                            """)


                    elif i != 'Current Balance' and i != 'Daily % Change' and i != '24hr Price Change %' and i != 'Current Value' and i != 'Average Daily Value Increase':
                        openfile.write(f"""
                                  <div class="col-6 col-xl-6">
                                      <div class="card" style="height:8rem;background-color: {small_tile_col};">
                                          <div class="card-body">
                                            <h4 class="card-title" style="font-size:24px"><strong>{data[item][i]}</strong></h4>
                                            <h6 class="card-subtitle mb-2 text-muted">{i}</h6>
                                          </div>
                                    </div>
                                  </div>

                            """)
            openfile.write("""
                </div>
                                  </div>
                  </div>
              </div>
                """)
        openfile.write("""
                </div>
        
      </div>
    </div>
          <!--   Core JS Files   -->
      <script src="assets/js/core/jquery.min.js"></script>
      <script src="assets/js/core/popper.min.js"></script>
      <script src="assets/js/core/bootstrap.min.js"></script>
      <script src="assets/js/plugins/perfect-scrollbar.jquery.min.js"></script>
      <!--  Google Maps Plugin    -->
      <!-- Place this tag in your head or just before your close body tag. -->

      <!-- Chart JS -->
      <script src="assets/js/plugins/chartjs.min.js"></script>
      <!--  Notifications Plugin    -->
      <script src="assets/js/plugins/bootstrap-notify.js"></script>
      <!-- Control Center for Black Dashboard: parallax effects, scripts for the example pages etc -->
      <script src="assets/js/black-dashboard.min.js?v=1.0.0"></script><!-- Black Dashboard DEMO methods, don't include it in your project! -->



    </div>
    </div>
      <script src="graphing/libs/chart.min.js"></script>
      <script src="graphing/libs/d3.v6.min.js"></script>
      <script src="graphing/sketch.js"></script>
      </body>
    </html>
             """)
# import json
# with open('../output.json','r') as outy:
#     make_html(json.load(outy),'../docs/index.html')