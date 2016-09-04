window.onload = function () {
		// Any of the following formats may be used
		var ctx = document.getElementById("racechart");
		var racechart = new Chart(ctx, {
			type: 'pie',
			data: {
				labels: ["Black/African American", "American Indian/Alaska Native","Asian","Native Hawaiian/Other Pacific Islander","Hispanic","Multi-Racial","White"],
				datasets: [{
					label: 'Racial Makeup',
					data: [1.6,0.1,20,0.4,17.4,4.8,55.7],
					backgroundColor: [
						'rgba(255, 99, 132, 0.2)',
						'rgba(255, 176, 197, 0.2)',
						'rgba(255, 255, 97, 0.2)',
						'rgba(97, 255, 97, 0.2)',
						'rgba(97, 176, 255, 0.2)',
						'rgba(136, 97, 255, 0.2)',
						'rgba(176, 97, 255, 0.2)',
					],
					borderColor: [
						'rgba(255, 99, 132, 1)',
						'rgba(255, 176, 197, 1)',
						'rgba(255, 255, 97, 1)',
						'rgba(97, 255, 97, 1)',
						'rgba(97, 176, 255, 1)',
						'rgba(136, 97, 255, 1)',
						'rgba(176, 97, 255, 1)',
					],
					borderWidth: 1.5
				}]
			},
			options: {
				scales: {
					
				}
			}
		});
		var ctx_2 = document.getElementById("nationalmerit");
		var nationalmerit = new Chart(ctx_2, {
			type: 'line',
			data: {
				labels: ["2013", "2014", "2015", "2016"],
			    datasets: [
			        {
			            label: "Commended",
			            fill: false,
			            lineTension: 0.1,
			            backgroundColor: "rgba(255, 99, 132, 0.2)",
			            borderColor: "rgba(255, 99, 132, 1)",
			            borderCapStyle: 'butt',
			            borderDash: [],
			            borderDashOffset: 0.0,
			            borderJoinStyle: 'miter',
			            pointBorderColor: "rgba(255, 99, 132, 1)",
			            pointBackgroundColor: "#fff",
			            pointBorderWidth: 1,
			            pointHoverRadius: 5,
			            pointHoverBackgroundColor: "rgba(255, 99, 132, 1)",
			            pointHoverBorderColor: "rgba(220,220,220,1)",
			            pointHoverBorderWidth: 2,
			            pointRadius: 1,
			            pointHitRadius: 10,
			            data: [44,49,50,64],
			            spanGaps: false,
			        },
			        {
			            label: "Semifinalist",
			            fill: false,
			            lineTension: 0.1,
			            backgroundColor: "rgba(255, 176, 197, 0.2)",
			            borderColor: "rgba(255, 176, 197, 1)",
			            borderCapStyle: 'butt',
			            borderDash: [],
			            borderDashOffset: 0.0,
			            borderJoinStyle: 'miter',
			            pointBorderColor: "rgba(255, 176, 197, 1)",
			            pointBackgroundColor: "#fff",
			            pointBorderWidth: 1,
			            pointHoverRadius: 5,
			            pointHoverBackgroundColor: "rgba(255, 176, 197, 1)",
			            pointHoverBorderColor: "rgba(220,220,220,1)",
			            pointHoverBorderWidth: 2,
			            pointRadius: 1,
			            pointHitRadius: 10,
			            data: [26,32,33,33],
			            spanGaps: false,
			        },
			        {
			            label: "Finalist",
			            fill: false,
			            lineTension: 0.1,
			            backgroundColor: "rgba(97, 255, 97, 0.2)",
			            borderColor: "rgba(97, 255, 97, 1)",
			            borderCapStyle: 'butt',
			            borderDash: [],
			            borderDashOffset: 0.0,
			            borderJoinStyle: 'miter',
			            pointBorderColor: "rgba(97, 255, 97, 1)",
			            pointBackgroundColor: "#fff",
			            pointBorderWidth: 1,
			            pointHoverRadius: 5,
			            pointHoverBackgroundColor: "rgba(97, 255, 97, 1)",
			            pointHoverBorderColor: "rgba(220,220,220,1)",
			            pointHoverBorderWidth: 2,
			            pointRadius: 1,
			            pointHitRadius: 10,
			            data: [26,29,31,31],
			            spanGaps: false,
			        },
			        {
			            label: "National Hispanic Recognition",
			            fill: false,
			            lineTension: 0.1,
			            backgroundColor: "rgba(97, 176, 255, 0.2)",
			            borderColor: "rgba(97, 176, 255, 1)",
			            borderCapStyle: 'butt',
			            borderDash: [],
			            borderDashOffset: 0.0,
			            borderJoinStyle: 'miter',
			            pointBorderColor: "rgba(97, 176, 255, 1)",
			            pointBackgroundColor: "#fff",
			            pointBorderWidth: 1,
			            pointHoverRadius: 5,
			            pointHoverBackgroundColor: "rgba(97, 176, 255, 1)",
			            pointHoverBorderColor: "rgba(220,220,220,1)",
			            pointHoverBorderWidth: 2,
			            pointRadius: 1,
			            pointHitRadius: 10,
			            data: [11,18,14,14],
			            spanGaps: false,
			        }
			    ]
			},
			options: {
				scales: {
					
				}
			}
		});
}