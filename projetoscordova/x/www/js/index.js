function initCrud() {
    const addForm = document.getElementById('addForm');
    const updateForm = document.getElementById('updateForm');
    const deleteForm = document.getElementById('deleteForm');
    const itemList = document.getElementById('itemList');

    // Event Listener para o formulário de adicionar
    addForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const data = document.getElementById('data').value;
        const dataNum = document.getElementById('data_num').value;
        addItem(data, dataNum);
        displayItems();
    });

    // Event Listener para o formulário de atualizar
    updateForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const id = parseInt(document.getElementById('update_id').value);
        const data = document.getElementById('update_data').value;
        const dataNum = document.getElementById('update_data_num').value;
        updateItem(id, data, dataNum);
        displayItems();
    });

    // Event Listener para o formulário de excluir
    deleteForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const id = parseInt(document.getElementById('delete_id').value);
        deleteItem(id);
        displayItems();
    });

    displayItems();
}

// Funções LocalStorage
function addItem(data, dataNum) {
    const items = getItems();
    const id = new Date().getTime();
    items.push({ id, data, dataNum });
    localStorage.setItem('items', JSON.stringify(items));
}

function getItems() {
    return JSON.parse(localStorage.getItem('items')) || [];
}

function updateItem(id, data, dataNum) {
    const items = getItems();
    const itemIndex = items.findIndex(item => item.id === id);
    if (itemIndex > -1) {
        items[itemIndex].data = data;
        items[itemIndex].dataNum = dataNum;
        localStorage.setItem('items', JSON.stringify(items));
    }
}

function deleteItem(id) {
    const items = getItems();
    const filteredItems = items.filter(item => item.id !== id);
    localStorage.setItem('items', JSON.stringify(filteredItems));
}

function displayItems() {
    const items = getItems();
    const itemList = document.getElementById('itemList');
    itemList.innerHTML = '';
    items.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `ID: ${item.id}, Data: ${item.data}, Data Num: ${item.dataNum}`;
        itemList.appendChild(li);
    });
}

// Funções IndexedDB
document.addEventListener('deviceready', function() {
    const request = indexedDB.open('myDatabase', 1);

    request.onupgradeneeded = function(event) {
        const db = event.target.result;
        const objectStore = db.createObjectStore('items', { keyPath: 'id' });
        objectStore.createIndex('data', 'data', { unique: false });
        objectStore.createIndex('dataNum', 'dataNum', { unique: false });
    };

    request.onsuccess = function(event) {
        const db = event.target.result;

        // Funções para IndexedDB
        function addItemIndexedDB(data, dataNum) {
            const transaction = db.transaction('items', 'readwrite');
            const objectStore = transaction.objectStore('items');
            const id = new Date().getTime();
            objectStore.add({ id, data, dataNum });
        }

        function updateItemIndexedDB(id, data, dataNum) {
            const transaction = db.transaction('items', 'readwrite');
            const objectStore = transaction.objectStore('items');
            const request = objectStore.get(id);
            request.onsuccess = function(event) {
                const item = event.target.result;
                item.data = data;
                item.dataNum = dataNum;
                objectStore.put(item);
            };
        }

        function deleteItemIndexedDB(id) {
            const transaction = db.transaction('items', 'readwrite');
            const objectStore = transaction.objectStore('items');
            objectStore.delete(id);
        }

        function displayItemsIndexedDB() {
            const transaction = db.transaction('items', 'readonly');
            const objectStore = transaction.objectStore('items');
            objectStore.getAll().onsuccess = function(event) {
                const items = event.target.result;
                const itemList = document.getElementById('itemList');
                itemList.innerHTML = '';
                items.forEach(item => {
                    const li = document.createElement('li');
                    li.textContent = `ID: ${item.id}, Data: ${item.data}, Data Num: ${item.dataNum}`;
                    itemList.appendChild(li);
                });
            };
        }

        // Atualizar funções de formulário para IndexedDB
        addForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const data = document.getElementById('data').value;
            const dataNum = document.getElementById('data_num').value;
            addItemIndexedDB(data, dataNum);
            displayItemsIndexedDB();
        });

        updateForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const id = parseInt(document.getElementById('update_id').value);
            const data = document.getElementById('update_data').value;
            const dataNum = document.getElementById('update_data_num').value;
            updateItemIndexedDB(id, data, dataNum);
            displayItemsIndexedDB();
        });

        deleteForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const id = parseInt(document.getElementById('delete_id').value);
            deleteItemIndexedDB(id);
            displayItemsIndexedDB();
        });

        displayItemsIndexedDB();
    };
});