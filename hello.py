import datetime

class Family:
    def __init__(self, family_code, family_name, waste_limit=100):
        self.family_code = family_code
        self.family_name = family_name
        self.waste_limit = waste_limit
        self.waste_records = []  # list of (date, waste_type, amount)

    def add_waste(self, waste_type, amount):
        today = datetime.date.today()
        self.waste_records.append((today, waste_type, amount))

    def total_waste(self):
        return sum(record[2] for record in self.waste_records)

    def waste_by_type(self):
        result = {}
        for _, waste_type, amount in self.waste_records:
            result[waste_type] = result.get(waste_type, 0) + amount
        return result

    def check_limit(self):
        total = self.total_waste()
        if total > self.waste_limit:
            extra = total - self.waste_limit
            fine = extra * 2  # fine per extra unit
            return True, fine
        return False, 0


class WasteManagementSystem:
    def __init__(self):
        self.families = {}

    def add_family(self, family_code, family_name, waste_limit=100):
        if family_code in self.families:
            print("Family code already exists!")
        else:
            self.families[family_code] = Family(family_code, family_name, waste_limit)
            print("Family added successfully!")

    def add_waste_record(self, family_code, waste_type, amount):
        if family_code in self.families:
            self.families[family_code].add_waste(waste_type, amount)
            print("Waste record added.")
        else:
            print("Family not found!")

    def monthly_report(self, family_code):
        if family_code in self.families:
            family = self.families[family_code]
            print("\n--- Monthly Report ---")
            print("Family:", family.family_name)
            print("Total Waste:", family.total_waste())
            print("Waste by Type:", family.waste_by_type())

            exceeded, fine = family.check_limit()
            if exceeded:
                print("Limit exceeded! Fine:", fine)
            else:
                print("Within waste limit.")
        else:
            print("Family not found!")


# --------- MAIN PROGRAM ---------
system = WasteManagementSystem()

while True:
    print("\n1. Add Family")
    print("2. Add Waste Record")
    print("3. View Monthly Report")
    print("4. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        code = input("Enter family code: ")
        name = input("Enter family name: ")
        limit = int(input("Enter monthly waste limit: "))
        system.add_family(code, name, limit)

    elif choice == "2":
        code = input("Enter family code: ")
        waste_type = input("Enter waste type (plastic/metal/etc): ")
        amount = float(input("Enter waste amount (kg): "))
        system.add_waste_record(code, waste_type, amount)

    elif choice == "3":
        code = input("Enter family code: ")
        system.monthly_report(code)

    elif choice == "4":
        print("Exiting system...")
        break

    else:
        print("Invalid choice!")
<!DOCTYPE html>
<html>
<head>
    <title>Waste Management System</title>
    <style>
        body {
            font-family: Arial;
            background: #f4f4f4;
            padding: 20px;
        }
        h2 {
            color: green;
        }
        .box {
            background: white;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0px 0px 5px gray;
        }
        input, select, button {
            padding: 8px;
            margin: 5px;
        }
        button {
            background: green;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background: darkgreen;
        }
        #report {
            background: #eef;
            padding: 10px;
            margin-top: 10px;
        }
    </style>
</head>
<body>

<h2>Waste Management System</h2>

<div class="box">
    <h3>Add Family</h3>
    <input type="text" id="familyCode" placeholder="Family Code">
    <input type="text" id="familyName" placeholder="Family Name">
    <input type="number" id="wasteLimit" placeholder="Monthly Waste Limit (kg)">
    <button onclick="addFamily()">Add Family</button>
</div>

<div class="box">
    <h3>Add Waste Record</h3>
    <input type="text" id="wasteFamilyCode" placeholder="Family Code">
    <select id="wasteType">
        <option value="Plastic">Plastic</option>
        <option value="Metal">Metal</option>
        <option value="Organic">Organic</option>
        <option value="Paper">Paper</option>
    </select>
    <input type="number" id="wasteAmount" placeholder="Amount (kg)">
    <button onclick="addWaste()">Add Waste</button>
</div>

<div class="box">
    <h3>Monthly Report</h3>
    <input type="text" id="reportFamilyCode" placeholder="Family Code">
    <button onclick="generateReport()">Generate Report</button>
    <div id="report"></div>
</div>

<script>
let families = JSON.parse(localStorage.getItem("families")) || {};

function saveData() {
    localStorage.setItem("families", JSON.stringify(families));
}

function addFamily() {
    let code = document.getElementById("familyCode").value;
    let name = document.getElementById("familyName").value;
    let limit = parseFloat(document.getElementById("wasteLimit").value);

    if (!code || !name || !limit) {
        alert("Please fill all fields");
        return;
    }

    if (families[code]) {
        alert("Family code already exists!");
        return;
    }

    families[code] = {
        name: name,
        limit: limit,
        waste: []
    };

    saveData();
    alert("Family added successfully!");
}

function addWaste() {
    let code = document.getElementById("wasteFamilyCode").value;
    let type = document.getElementById("wasteType").value;
    let amount = parseFloat(document.getElementById("wasteAmount").value);

    if (!families[code]) {
        alert("Family not found!");
        return;
    }

    families[code].waste.push({
        type: type,
        amount: amount
    });

    saveData();
    alert("Waste record added!");
}

function generateReport() {
    let code = document.getElementById("reportFamilyCode").value;
    let reportDiv = document.getElementById("report");

    if (!families[code]) {
        reportDiv.innerHTML = "Family not found!";
        return;
    }

    let family = families[code];
    let total = 0;
    let wasteByType = {};

    family.waste.forEach(record => {
        total += record.amount;
        wasteByType[record.type] = (wasteByType[record.type] || 0) + record.amount;
    });

    let fine = 0;
    if (total > family.limit) {
        fine = (total - family.limit) * 2; // fine rate per kg
    }

    let output = `
        <h4>Family: ${family.name}</h4>
        <p>Total Waste: ${total} kg</p>
        <p>Waste by Type:</p>
        <ul>
    `;

    for (let type in wasteByType) {
        output += `<li>${type}: ${wasteByType[type]} kg</li>`;
    }

    output += "</ul>";

    if (fine > 0) {
        output += `<p style="color:red;">Limit Exceeded! Fine: ₹${fine}</p>`;
    } else {
        output += `<p style="color:green;">Within Waste Limit</p>`;
    }

    reportDiv.innerHTML = output;
}
</script>

</body>
</html>
