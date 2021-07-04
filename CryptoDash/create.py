def make_html(data, path):
    with open(path, 'w') as openfile:
        openfile.write("""
        <!doctype html>
<html lang="en">
  <head>
    <title>Hello, world!</title>
    <!-- Required meta tags -->
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
     transform: scale(1.05);
  box-shadow: 0 10px 20px rgba(0,0,0,.12), 0 4px 8px rgba(0,0,0,.06);}
    </style>
  </head>
  <body>
  """+
        f"""
<div class="container-fluid">
  <div class="container" style="margin-top: 5%">

    <div class="content">
      <div class="container-fluid">
          <div class="row">
          <div class="col-12">
            <div class="card card-chart">
              <div class="card-header ">
                <div class="row">
                  <div class="col-sm-6 text-left">
                    <h5 class="card-category">Total gains $</h5>
                    <h2 class="card-title">${data['Totals']['Total']}</h2>
                  </div>
                </div>
              </div>
              <div class="card-body">
                <div class="chart-area">
                  <canvas id="canvas-total">

                  </canvas>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        """)


        for item in data.keys():
            if item != 'Totals':
                openfile.write(f"""
                <div class="card" style="padding: 2%;background-color: #1a1a28">
                          <div class="row">
                  <div class="col-12">
    
                      <h4 class="title" style="font-size:30px">{item}</h4>
                  </div>
                  <div class="col-sm-12 col-md-6 col-lg-6 col-xl-6">
                              <div class="card">
                                  <div class="card-body">
                                    <h4 class="card-title" style="font-size:24px"><strong>{data[item]['Current Balance']} {item}</strong></h4>
                                    <h6 class="card-subtitle mb-2 text-muted">Total</h6>
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
                    openfile.write(f"""
                          <div class="col-6 col-xl-6">
                              <div class="card">
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
    <footer class="footer">


         <!-- your footer here -->

    </footer>
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
