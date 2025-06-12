const buttons = document.getElementsByClassName('order_btn');
  const orderSum = document.getElementById('orderSum');
  let payment = 0;
  Array.from(buttons).forEach(btn => {
    btn.addEventListener('click', function addOrder() {
      const productName = btn.value;
      let quantity = prompt('количество?', 1);
      if (quantity !== null )
      fetch('/create-order/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': getCookie('csrftoken') // Получаем CSRF-токен
        },
        body: `product_name=${encodeURIComponent(productName)}&quantity=${quantity}`
      })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          const order = document.getElementById('order_inner');
          const order_main = document.getElementById('order');
          // order_main.classList.remove('d-none');
          // alert(`Заказ добавлен! ${data.product.name} ${quantity} шт.`);
          // Создаем новый элемент div
        const newOrderItem = document.createElement('div');
        newOrderItem.className = 'input-group input-group-sm mb-3';

        // Создаем элемент span
        const productName = document.createElement('span');
        productName.className = 'input-group-text fw-bold';
        productName.id = `inputGroup_${data.product.id}`;
        productName.textContent = `${data.product.name} (${data.product.size})`;
        productName.title=data.product.price*quantity+' руб.';
        productName.setAttribute('data-toggle',"tooltip");

        // Создаем элемент input
        const quantityInput = document.createElement('input');
        quantityInput.type = 'number';
        quantityInput.className = 'form-control input_order';
        quantityInput.setAttribute('aria-label', 'Sizing example input');
        quantityInput.setAttribute('aria-describedby', `inputGroup_${data.product.id}`);
        quantityInput.setAttribute('min',1);
        quantityInput.name = 'quantity';
        quantityInput.value = quantity;
        
        const hiddenIdInput = document.createElement('input');
        hiddenIdInput.type = 'hidden';
        hiddenIdInput.className = 'form-control input_order';
        hiddenIdInput.setAttribute('aria-label', 'Sizing example input');
        hiddenIdInput.setAttribute('aria-describedby', `inputGroup_${data.product.id}`);
        hiddenIdInput.name = 'product_id';
        hiddenIdInput.value = data.product.id;
        // Создаем кнопку удаления
        const deleteButton = document.createElement('button');
        deleteButton.className = 'btn btn-sm btn-danger';
        deleteButton.textContent = '✕';
        payment += data.product.price*quantityInput.value;
        orderSum.innerText=payment;
        // Добавляем обработчик события для кнопки удаления
        deleteButton.addEventListener('click', () => {
            order.removeChild(newOrderItem);
            payment -= data.product.price*quantityInput.value;
            orderSum.innerText=payment;
            const input_groups = document.getElementsByClassName('input-group');
            if (input_groups.length === 0) order_main.classList.add('d-none');
        });
        
        quantityInput.addEventListener('click', ()=>{
          payment += data.product.price*(quantityInput.value - quantity);
          orderSum.innerText=payment;
          quantity = quantityInput.value;
          productName.setAttribute('data-bs-original-title',data.product.price*quantity+' руб.');
        //   initializeTooltips();
        })

        // Добавляем элементы в новый div
        newOrderItem.appendChild(productName);
        newOrderItem.appendChild(quantityInput);
        newOrderItem.appendChild(hiddenIdInput);
        newOrderItem.appendChild(deleteButton); // Добавляем кнопку удаления

        // Добавляем новый div в order
        order.appendChild(newOrderItem);
        initializeTooltips();
        } else {
          alert(`Ошибка при создании заказа.`);
        }
      })
      .catch(error => {
        console.error('Ошибка:', error);
        document.getElementById('result').innerHTML = 'Ошибка сети.';
      });
    })
  });

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Проверяем, начинается ли cookie с нужного имени
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  toggleBtn = document.querySelector('.shower > button');
  toggleBtn.addEventListener('click', function () {
    const order_main = document.getElementById('order');
    const icon = toggleBtn.querySelector('i');
    if (order_main.classList.contains('d-none')) {
            order_main.classList.remove('d-none'); // Убираем класс, чтобы показать элемент
            order_main.classList.add('d-block'); // Добавляем класс, чтобы установить display: block
            icon.classList.remove('bi-eye-fill');
            icon.classList.add('bi-eye-slash-fill');
        } else {
            order_main.classList.remove('d-block'); // Убираем класс, чтобы скрыть элемент
            order_main.classList.add('d-none'); // Добавляем класс, чтобы установить display: none
            icon.classList.add('bi-eye-fill');
            icon.classList.remove('bi-eye-slash-fill');
        }
  })