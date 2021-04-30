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
                  :label="$t(`table-data.description`)"
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
            <v-btn color="primary" :disabled="!isPrint" @click="generatePDF">
              {{ $t("table-data.print") }}
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

    <template v-slot:[`header.id`]="">
      {{ $t("pdf.transaction-id") }}
    </template>
    <template v-slot:[`header.customerNo`]="">
      {{ $t(`pdf.customer-no`) }}
    </template>
    <template v-slot:[`header.customerName`]="">
      {{ $t(`pdf.customer-name`) }}
    </template>
    <template v-slot:[`header.taxID`]="">
      {{ $t(`pdf.tax-id`) }}
    </template>
    <template v-slot:[`header.vatID`]="">
      {{ $t(`pdf.vat-id`) }}
    </template>
    <template v-slot:[`header.material`]="">
      {{ $t(`pdf.material`) }}
    </template>
    <template v-slot:[`header.netWeight`]="">
      {{ $t(`pdf.net-weight`) }}
    </template>
    <template v-slot:[`header.pricePerKg`]="">
      {{ $t(`pdf.price-per-kg`) }}
    </template>
    <template v-slot:[`header.positionValue`]="">
      {{ $t(`pdf.position-value`) }}
    </template>
    <template v-slot:[`header.vatAmount`]="">
      {{ $t(`pdf.vat-amount`) }}
    </template>
    <template v-slot:[`header.grossAmount`]="">
      {{ $t(`pdf.gross-amount`) }}
    </template>
  </v-data-table>
</template>

<script>
import { getReportsData } from '../../api'
import jsPDF from 'jspdf'
// import moment from "moment";
export default {
  name: 'reports',
  data: () => ({
    headers: [
      { text: 'Transaction-ID', value: 'id' },
      { text: 'Customer-No', value: 'customerNo' },
      { text: 'Customer Name', value: 'customerName' },
      { text: 'Tax-ID', value: 'taxID' },
      { text: 'VAT-ID', value: 'vatID' },
      // { text: "Car-Licenseplate-NO", value: "cln" },
      // { text: "Material Category", value: "" },
      { text: 'Material', value: 'material' },
      { text: 'Net-Weight', value: 'netWeight' },
      { text: 'Price-per-Kg', value: 'pricePerKg' },
      { text: 'Position Value', value: 'positionValue' },
      { text: 'VAT Amount', value: 'vatAmount' },
      { text: 'Gross Amount', value: 'grossAmount' }
    ],
    items: [],
    date: '',
    isPrint: false,
    fromDateMenu: false,
    token: ''
  }),

  created () {
    this.initialize()
  },

  methods: {
    initialize () {
      this.token = document
        .querySelector('input[name="csrfmiddlewaretoken"]')
        .getAttribute('value')
    },
    onChangeDate () {
      if (this.date) {
        getReportsData(this.date, this.token)
          .then((res) => res.json())
          .then(({ result }) => {
            if (result.length > 0) {
              this.isPrint = true
              this.items = result.map((item) => ({
                id: item.id,
                customerNo: item.arrival.customer.id,
                customerName:
                  item.arrival.customer.firstname +
                  ' ' +
                  item.arrival.customer.lastname,
                taxID: item.arrival.customer.company
                  ? item.arrival.customer.company.tax_id
                  : '',
                vatID: item.arrival.customer.company
                  ? item.arrival.customer.company.vat_id
                  : '',
                // CLN: item.CLN,
                // materialCategory: item.category,
                material: item.arrival.arrival_pos[0].material.name,
                netWeight: item.arrival.arrival_pos[0].net_weight_kg,
                pricePerKg: item.arrival.arrival_pos[0].material.price_per_kg,
                positionValue: (
                  item.arrival.arrival_pos[0].net_weight_kg *
                  item.arrival.arrival_pos[0].material.price_per_kg
                ).toFixed(2),
                vatAmount: item.vat_amount,
                grossAmount: (
                  item.vat_amount +
                  item.arrival.arrival_pos[0].net_weight_kg *
                    item.arrival.arrival_pos[0].material.price_per_kg
                ).toFixed(2)
              }))
            }
          })
      }
    },
    generatePDF () {
      const pdfName = 'report_' + this.date.replaceAll('-', '').trim()

      const addPages = (doc) => {
        const pageCount = doc.internal.getNumberOfPages()

        for (var i = 1; i <= pageCount; i++) {
          doc.setPage(i)
          // Header
          doc.setFont('helvetica', 'Bold')
          doc.setFontSize(30)
          doc.text(this.$t('pdf.title'), doc.internal.pageSize.width / 2, 30, {
            align: 'center'
          })
          doc.setFont('helvetica')
          doc.setFontSize(10)
          doc.text(
            `${this.$t('pdf.date')}: ` + this.date,
            doc.internal.pageSize.width - 10,
            30,
            {
              align: 'right'
            }
          )
          doc.setDrawColor('gray')
          doc.setLineWidth(0, 5)
          doc.line(10, 35, doc.internal.pageSize.width - 10, 35)
          // Body
          for (let j = 0; j < 5; j++) {
            const index = (i - 1) * 5 + j
            if (index < this.items.length) {
              const height = j * 50 + 45
              doc.setFont('helvetica')
              doc.setFontSize(10)
              doc.text(this.$t('pdf.transaction-id'), 10, height)
              doc.text(this.$t('pdf.customer-no'), 40, height)
              doc.text(this.$t('pdf.customer-name'), 65, height)
              doc.text(this.$t('pdf.tax-id'), 100, height)
              doc.text(this.$t('pdf.vat-id'), 130, height)
              doc.text(this.$t('pdf.car-license-number'), 160, height)

              doc.text(this.$t('pdf.material'), 10, height + 20)
              doc.text(this.$t('pdf.net-weight'), 40, height + 20)
              doc.text(this.$t('pdf.price-per-kg'), 70, height + 20)
              doc.text(this.$t('pdf.position-value'), 100, height + 20)
              doc.text(this.$t('pdf.vat-amount'), 130, height + 20)
              doc.text(this.$t('pdf.gross-amount'), 160, height + 20)
            }
          }

          for (let j = 0; j < 5; j++) {
            const index = (i - 1) * 5 + j
            if (index < this.items.length) {
              const height = j * 50 + 45

              doc.setFont('helvetica', 'bold')
              doc.setFontSize(10)
              doc.text(`${this.items[index].id}`, 20, height + 5)
              doc.text(`${this.items[index].customerNo}`, 48, height + 5)
              doc.text(`${this.items[index].customerName}`, 65, height + 5)
              doc.text(`${this.items[index].taxID}`, 100, height + 5)
              doc.text(`${this.items[index].vatID}`, 130, height + 5)
              doc.text('123456', 160, height + 5)

              doc.text(`${this.items[index].material}`, 10, height + 25)
              doc.text(`${this.items[index].netWeight} kg`, 40, height + 25)
              doc.text(`${this.items[index].pricePerKg} EUR`, 70, height + 25)
              doc.text(
                `${this.items[index].positionValue} EUR`,
                100,
                height + 25
              )
              doc.text(`${this.items[index].vatAmount} EUR`, 130, height + 25)
              doc.text(
                `${this.items[index].grossAmount} EUR`,
                160,
                height + 25
              )
            }
          }
          // Footer
          doc.setFont('helvetica', 'italic')
          doc.setFontSize(10)
          // doc.setDrawColor("gray");
          // doc.setLineWidth(0, 5);
          // doc.line(10, 282, doc.internal.pageSize.width - 10, 282);
          doc.text(
            'Page ' + String(i) + ' of ' + String(pageCount),
            doc.internal.pageSize.width / 2,
            287,
            {
              align: 'center'
            }
          )
        }
      }

      const doc = new jsPDF()
      const pageNum = Number(this.items.length / 5) - 1

      for (let i = 0; i < pageNum; i++) {
        doc.addPage()
      }

      // doc.text("text");
      // doc.autoTable(...)
      addPages(doc)
      doc.save(pdfName + '.pdf')
    }
  }
}
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
