// bar graph dashboard

const appointmentsData = {
    labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
    datasets: [
      {
        label: 'Doctor',
        data: [20, 30, 25, 35, 40],
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1
      },
      {
        label: 'Salon',
        data: [15, 25, 20, 30, 35],
        backgroundColor: 'rgba(255, 205, 86, 0.2)',
        borderColor: 'rgba(255, 205, 86, 1)',
        borderWidth: 1
      },
      {
        label: 'Corporate',
        data: [10, 20, 15, 25, 30],
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1
      },
      {
        label: 'Government',
        data: [25, 35, 30, 40, 45],
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1
      }
    ]
  };

  // Chart configuration
  const config = {
    type: 'bar',
    data: appointmentsData,
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    },
  };

  // Create chart
  var myChart = new Chart(
    document.getElementById('appointmentChart'),
    config
  );
  
  // pie chart for total expenses

  const totalExpenses = 12000; // Total expenses in Rupees

  // Adjusted expenses for each category to sum up to 12000
  const expensesData = {
    labels: ['Doctor', 'Salon', 'Corporate', 'Government'],
    datasets: [{
      data: [0.25 * totalExpenses, 0.2 * totalExpenses, 0.15 * totalExpenses, 0.4 * totalExpenses],
      backgroundColor: ['rgba(255, 99, 132, 0.2)', 'rgba(255, 205, 86, 0.2)', 'rgba(75, 192, 192, 0.2)', 'rgba(54, 162, 235, 0.2)'],
      borderColor: ['rgba(255, 99, 132, 1)', 'rgba(255, 205, 86, 1)', 'rgba(75, 192, 192, 1)', 'rgba(54, 162, 235, 1)'],
      borderWidth: 1
    }]
  };

  const config1 = {
    type: 'pie',
    data: expensesData,
    options: {
      plugins: {
        title: {
          display: true,
          text: 'Appointment Expenses Distribution'
        }
      }
    },
  };

  var myChart = new Chart(
    document.getElementById('expensesChart'),
    config1
  );

  // calender javascript

  let currentDate = new Date();
  let currentYear = currentDate.getFullYear();
  let currentMonth = currentDate.getMonth();

  function generateCalendar(year, month) {
    let firstDay = new Date(year, month, 1).getDay();
    let lastDate = new Date(year, month + 1, 0).getDate();
    let currentDate = new Date();
    let selectedDate = null;

    let tableBody = document.querySelector('.calendar tbody');
    tableBody.innerHTML = '';

    let row = document.createElement('tr');

    for (let i = 0; i < firstDay; i++) {
      let cell = document.createElement('td');
      row.appendChild(cell);
    }

    for (let i = 1; i <= lastDate; i++) {
      let cell = document.createElement('td');
      cell.textContent = i;

      if (year === currentDate.getFullYear() && month === currentDate.getMonth() && i === currentDate.getDate()) {
        cell.classList.add('today');
      }

      cell.addEventListener('click', function() {
        if (selectedDate) {
          selectedDate.classList.remove('selected');
        }
        selectedDate = this;
        selectedDate.classList.add('selected');

        document.getElementById('selected-date').textContent = `${i}-${month + 1}-${year}`;
        displayAppointments(i, month + 1, year);
      });

      row.appendChild(cell);

      if ((i + firstDay) % 7 === 0 || i === lastDate) {
        tableBody.appendChild(row);
        row = document.createElement('tr');
      }
    }

    // Update current month and year display
    document.getElementById('current-month-year').textContent = `${getMonthName(month)} ${year}`;
  }

  function getMonthName(month) {
    const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    return months[month];
  }

  function displayAppointments(day, month, year) {
    let appointments = [
      'Appointment 1',
      'Appointment 2',
      'Appointment 3'
    ];

    let appointmentsList = document.getElementById('appointments-list');
    appointmentsList.innerHTML = '';

    appointments.forEach(appointment => {
      let listItem = document.createElement('li');
      listItem.textContent = appointment;
      appointmentsList.appendChild(listItem);
    });
  }

  generateCalendar(currentYear, currentMonth);

  document.getElementById('prev-month').addEventListener('click', function() {
    currentMonth--;
    if (currentMonth < 0) {
      currentYear--;
      currentMonth = 11;
    }
    generateCalendar(currentYear, currentMonth);
  });

  document.getElementById('next-month').addEventListener('click', function() {
    currentMonth++;
    if (currentMonth > 11) {
      currentYear++;
      currentMonth = 0;
    }
    generateCalendar(currentYear, currentMonth);
  });

  document.getElementById('prev-year').addEventListener('click', function() {
    currentYear--;
    generateCalendar(currentYear, currentMonth);
  });

  document.getElementById('next-year').addEventListener('click', function() {
    currentYear++;
    generateCalendar(currentYear, currentMonth);
  });

  document.getElementById('add-appointment').addEventListener('click', function() {
    alert('Add Appointment functionality not implemented.');
  });


  
  //end here
  // application form
  // Function to check availability and update status
function checkAvailability() {
  // Perform availability check logic here
  // For demonstration, let's assume availability is checked asynchronously
  // Simulate a delay of 1 second
  setTimeout(function() {
      // Display availability status
      var availabilityStatus = document.getElementById('availabilityStatus');
      availabilityStatus.innerHTML = '<div class="alert alert-success" role="alert">Appointment available at selected date and time!</div>';
  }, 1000);
}

// Attach event listener to the appointment form submit button
document.querySelector('#appointmentForm').addEventListener('submit', function(event) {
  // Prevent the default form submission behavior
  event.preventDefault();
  
  // Call function to check availability
  checkAvailability();
});
//end application form

//Book Appointment dropdown
function selectOption(option) {
  console.log("Selected option: " + option);
  // koi action perform kro yaha if koi option select ho
}
//
  
 
