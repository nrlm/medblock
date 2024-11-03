// Mengambil data blockchain dan menampilkan sepuluh transaksi terakhir
async function getChain() {
    try {
        const response = await fetch('/chain');
        const data = await response.json();
        
        // Menampilkan data blockchain keseluruhan
        document.getElementById('chain').textContent = JSON.stringify(data, null, 2);
        
        // Mengambil dan menampilkan hingga sepuluh transaksi terakhir
        const transactionsList = [];
        for (let i = data.chain.length - 1; i >= 0 && transactionsList.length < 10; i--) {
            const block = data.chain[i];
            for (let j = block.transactions.length - 1; j >= 0 && transactionsList.length < 10; j--) {
                transactionsList.push(block.transactions[j]);
            }
        }

        // Menampilkan transaksi terakhir
        if (transactionsList.length > 0) {
            document.getElementById('last-transactions').textContent = JSON.stringify(transactionsList, null, 2);
        } else {
            document.getElementById('last-transactions').textContent = "No transactions in the blockchain.";
        }
    } catch (error) {
        console.error("Error fetching chain data:", error);
    }
}

// Fungsi untuk menambah transaksi baru
async function addTransaction() {
    const transaction = {
        sender: document.getElementById('sender').value,
        receiver: document.getElementById('receiver').value,
        amount: parseInt(document.getElementById('amount').value),
        type: document.getElementById('type').value
    };

    try {
        await fetch('/transactions/new', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(transaction)
        });
        getChain();  // Memperbarui daftar transaksi terbaru setelah menambah transaksi
    } catch (error) {
        console.error("Error adding transaction:", error);
    }
}
