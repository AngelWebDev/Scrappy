<template>
  <v-data-table :headers="headers" :items="items" class="elevation-1">
    <template v-slot:top>
      <v-toolbar flat>
        <v-row class="mt-12 mb-8 pt-8 pb-4">
          <v-col cols="6">
            <v-menu
              v-model="fromDateMenu"
              :close-on-content-click="false"
              :nudge-right="20"
              transition="scale-transition"
              offset-y
              full-width
              max-width="290px"
              min-width="290px"
            >
              <template v-slot:activator="{ on }">
                <v-text-field
                  label="Select the Transaction Date"
                  readonly
                  :value="date"
                  v-on="on"
                ></v-text-field>
              </template>
              <v-date-picker
                locale="en-in"
                v-model="date"
                no-title
                @change="onChangeDate"
                @input="fromDateMenu = false"
              ></v-date-picker>
            </v-menu>
          </v-col>
          <v-col cols="6" class="text-right">
            <v-btn
              color="primary"
              :disabled="date ? false : true"
              @click="generatePDF"
            >
              Print
            </v-btn>
          </v-col>
        </v-row>
      </v-toolbar>
    </template>

    <template v-slot:no-data>
      <v-btn color="primary" @click="initialize">
        Reset
      </v-btn>
    </template>
  </v-data-table>
</template>

<script>
import { getReportsData } from "../../api";
import jsPDF from "jspdf";
// import moment from "moment";
export default {
  name: "reports",
  data: () => ({
    headers: [
      { text: "Transaction-ID", value: "id" },
      { text: "Customer-No", value: "customerNo" },
      { text: "Customer Name", value: "customerName" },
      { text: "Tax-ID", value: "taxID" },
      { text: "VAT-ID", value: "vatID" },
      // { text: "Car-Licenseplate-NO", value: "cln" },
      // { text: "Material Category", value: "" },
      { text: "Material", value: "material" },
      { text: "Net-Weight", value: "netWeight" },
      { text: "Price-per-Kg", value: "pricePerKg" },
      { text: "Position Value", value: "positionValue" },
      { text: "VAT Amount", value: "vatAmount" },
      { text: "Gross Amount", value: "grossAmount" },
    ],
    items: [],
    date: "",
    fromDateMenu: false,
    token: "",
  }),

  created() {
    this.initialize();
  },

  methods: {
    initialize() {
      this.token = document
        .querySelector('input[name="csrfmiddlewaretoken"]')
        .getAttribute("value");
    },
    onChangeDate() {
      getReportsData(this.token)
        .then((res) => res.json())
        .then(({ result }) => {
          this.items = result.map((item) => ({
            id: item.id,
            customerNo: item.customer.id,
            customerName:
              item.customer.firstname + " " + item.customer.lastname,
            taxID: item.customer.company ? item.customer.company.tax_id : "",
            vatID: item.customer.company ? item.customer.company.vat_id : "",
            // CLN: item.CLN,
            // materialCategory: item.category,
            material: item.material.name,
            netWeight: item.net_weight,
            pricePerKg: item.price_per_kg,
            positionValue: item.net_weight * item.price_per_kg,
            vatAmount: item.vat_amount,
            grossAmount: item.vat_amount + item.net_weight * item.price_per_kg,
          }));
        });
    },
    generatePDF() {
      let pdfName = "report_" + this.date.replaceAll("-", "").trim();

      const addPages = (doc) => {
        const pageCount = doc.internal.getNumberOfPages();

        for (var i = 1; i <= pageCount; i++) {
          doc.setPage(i);
          //Header
          doc.setFont("helvetica", "Bold");
          doc.setFontSize(30);
          doc.text("Trödlerbuch", doc.internal.pageSize.width / 2, 30, {
            align: "center",
          });
          doc.setFont("helvetica");
          doc.setFontSize(10);
          doc.text("Date: " + this.date, doc.internal.pageSize.width - 10, 30, {
            align: "right",
          });
          doc.setDrawColor("gray");
          doc.setLineWidth(0, 5);
          doc.line(10, 35, doc.internal.pageSize.width - 10, 35);
          //Body
          for (let j = 0; j < 5; j++) {
            let index = (i - 1) * 5 + j;
            if (index < this.items.length) {
              let height = j * 50 + 45;
              doc.setFont("helvetica");
              doc.setFontSize(10);
              doc.text("Transaction-ID", 10, height);
              doc.text("Customer-No", 40, height);
              doc.text("Customer Name", 65, height);
              doc.text("Tax ID", 100, height);
              doc.text("VAT ID", 130, height);
              doc.text("Car Licenseplate Number", 160, height);

              doc.text("Material", 10, height + 20);
              doc.text("Net-Weight", 40, height + 20);
              doc.text("Price_per_kg", 70, height + 20);
              doc.text("Position Value", 100, height + 20);
              doc.text("Vat Amount", 130, height + 20);
              doc.text("Gross Amount", 160, height + 20);
            }
          }

          for (let j = 0; j < 5; j++) {
            let index = (i - 1) * 5 + j;
            if (index < this.items.length) {
              let height = j * 50 + 45;

              doc.setFont("helvetica", "bold");
              doc.setFontSize(10);
              doc.text(`${this.items[index].id}`, 20, height + 5);
              doc.text(`${this.items[index].customerNo}`, 48, height + 5);
              doc.text(`${this.items[index].customerName}`, 65, height + 5);
              doc.text(`${this.items[index].taxID}`, 100, height + 5);
              doc.text(`${this.items[index].vatID}`, 130, height + 5);
              doc.text(`123456`, 160, height + 5);

              doc.text(`${this.items[index].material}`, 10, height + 25);
              doc.text(`${this.items[index].netWeight} kg`, 40, height + 25);
              doc.text(`${this.items[index].pricePerKg} EUR`, 70, height + 25);
              doc.text(
                `${this.items[index].positionValue} EUR`,
                100,
                height + 25
              );
              doc.text(`${this.items[index].vatAmount} EUR`, 130, height + 25);
              doc.text(
                `${this.items[index].grossAmount} EUR`,
                160,
                height + 25
              );
            }
          }
          //Footer
          doc.setFont("helvetica", "italic");
          doc.setFontSize(10);
          // doc.setDrawColor("gray");
          // doc.setLineWidth(0, 5);
          // doc.line(10, 282, doc.internal.pageSize.width - 10, 282);
          doc.text(
            "Page " + String(i) + " of " + String(pageCount),
            doc.internal.pageSize.width / 2,
            287,
            {
              align: "center",
            }
          );
        }
      };

      let doc = new jsPDF();
      const pageNum = Number(this.items.length / 5) - 1;

      for (let i = 0; i < pageNum; i++) {
        doc.addPage();
      }

      // doc.text("text");
      // doc.autoTable(...)
      addPages(doc);
      doc.save(pdfName + ".pdf");
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.v-data-table {
  margin-left: 260px;
}
.invite-error {
  color: white !important;
  padding-top: 10px !important;
}
</style>
