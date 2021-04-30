<template>
  <v-data-table
    :headers="headers"
    :items="items"
    :search="search"
    class="elevation-1"
    @click:row="editItem"
  >
    <template v-slot:top>
      <v-toolbar flat>
        <v-text-field
          v-model="search"
          label="Search"
          single-line
          hide-details
        />
        <v-spacer></v-spacer>
        <v-dialog v-model="dialog" max-width="800px">
          <v-card>
            <v-card-title>
              <span class="headline">{{ $t(`side-bar.arrival_details`) }}</span>
            </v-card-title>
            <v-card-text>
              <v-container>
                <v-row>
                  <v-data-table
                    :headers="arrivalsHeader"
                    :items="arrivals"
                    :search="search"
                    :hide-default-footer="true"
                    class="elevation-2"
                    @click:row="selectMaterial"
                  >
                  </v-data-table>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-title>
              <span class="headline">{{ $t(`side-bar.payout`) }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="6"></v-col>
                  <v-col cols="6" class="text-left">
                    <h3>{{ $t("table-data.customer") }}</h3>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" sm="6" md="6">
                    <v-row class="text-left pa-2 ma-0">
                      <v-col class="text-left pa-0 ma-0">
                        <span class="doc_title">
                          {{ $t("table-data.material") }} :
                        </span>
                      </v-col>
                      <v-col class="text-left pa-0 ma-0">
                        <strong>
                          {{ editedItem.material.name }}
                        </strong>
                      </v-col>
                    </v-row>

                    <v-row class="text-left pa-2 ma-0">
                      <v-col class="text-left pa-0 ma-0">
                        <span class="doc_title">
                          {{ $t("table-data.arrival") }} :
                        </span>
                      </v-col>
                      <v-col class="text-left pa-0 ma-0">
                        <strong>
                          {{ editedItem.arrived_at }}
                        </strong>
                      </v-col>
                    </v-row>

                    <v-row class="text-left pa-2 ma-0">
                      <v-col class="text-left pa-0 ma-0">
                        <span class="doc_title">
                          {{ $t("table-data.weight") }} :
                        </span>
                      </v-col>
                      <v-col
                        class="text-left pa-0 ma-0"
                        v-if="editedItem.net_weight_kg"
                      >
                        <strong>
                          {{ editedItem.net_weight_kg }}
                          kg
                        </strong>
                      </v-col>
                    </v-row>

                    <v-row class="text-left pa-2 ma-0">
                      <v-col class="text-left pa-0 ma-0">
                        <span class="doc_title">
                          {{ $t("table-data.value") }} :
                        </span>
                      </v-col>
                      <v-col
                        class="text-left pa-0 ma-0"
                        v-if="editedItem.payout"
                      >
                        <h2>{{ editedItem.payout }} EUR</h2>
                      </v-col>
                    </v-row>

                    <v-row class="text-left pa-2 ma-0">
                      <v-col class="text-left pa-0 ma-0">
                        <span class="doc_title">
                          {{ $t("table-data.paid_out") }} :
                        </span>
                      </v-col>
                      <v-col class="text-left pa-0 ma-0">
                        <strong>
                          {{ editedItem.paid_at }}
                        </strong>
                      </v-col>
                    </v-row>

                    <v-row class="text-left pa-2 ma-0">
                      <v-col class="text-left pa-0 ma-0">
                        <span class="doc_title">
                          {{ $t("table-data.paid_out_by") }} :
                        </span>
                      </v-col>
                      <v-col class="text-left pa-0 ma-0">
                        <strong>
                          {{ editedItem.username }}
                        </strong>
                      </v-col>
                    </v-row>
                  </v-col>

                  <v-col cols="12" sm="6" md="6">
                    <v-row class="text-left pa-2 ma-0">
                      <v-col class="text-left pa-0 ma-0">
                        <span class="doc_title">
                          {{ $t("table-data.name") }} :
                        </span>
                      </v-col>
                      <v-col class="text-left pa-0 ma-0">
                        <strong>
                          {{ editedItem.arrival.customer }}
                        </strong>
                      </v-col>
                    </v-row>
                    <v-row class="text-left pa-2 ma-0">
                      <v-col class="text-left pa-0 ma-0">
                        <span class="doc_title">
                          {{ $t("table-data.company") }} :
                        </span>
                      </v-col>
                      <v-col class="text-left pa-0 ma-0">
                        <strong>
                          {{ editedItem.arrival.company_name }}
                        </strong>
                      </v-col>
                    </v-row>
                    <v-row class="text-left pa-2 ma-0">
                      <v-col class="text-left pa-0 ma-0">
                        <span class="doc_title">
                          {{ $t("table-data.address") }} :
                        </span>
                      </v-col>
                      <v-col class="text-left pa-0 ma-0">
                        <strong>
                          {{ editedItem.arrival.street }}
                        </strong>
                      </v-col>
                    </v-row>
                    <v-row class="text-left pa-2 ma-0">
                      <v-col class="text-left pa-0 ma-0">
                        <span class="doc_title">
                          {{ $t("table-data.zip") }}/{{
                            $t("table-data.city")
                          }}:
                        </span>
                      </v-col>
                      <v-col class="text-left pa-0 ma-0">
                        <strong>
                          {{ editedItem.arrival.zip }}/{{
                            editedItem.arrival.city
                          }}
                        </strong>
                      </v-col>
                    </v-row>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-col class="text-center" cols="2">
                <v-btn color="red darken-1" text @click="close">
                  {{ $t("form-data.close") }}
                </v-btn>
              </v-col>
              <v-col class="text-center" cols="10">
                <v-btn color="blue darken-1" text @click="print">
                  {{ $t("form-data.print-receipt") }}
                </v-btn>
                <v-btn color="blue darken-1" text @click="email">
                  {{ $t("form-data.email-receipt") }}
                </v-btn>
                <v-btn color="red darken-1" text @click="reversal">
                  {{ $t("form-data.reversal") }}
                </v-btn>
              </v-col>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <v-dialog v-model="isEmail" max-width="500px">
          <v-card>
            <v-card-title>
              <span class="headline">{{ $t(`payout.send-receipt`) }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12" class="text-left">
                    <v-text-field
                      outlined
                      v-model="emailAddress"
                      :label="$t('table-data.email')"
                    />
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-col class="text-center">
                <v-btn color="red darken-1" text @click="sendEmail">
                  {{ $t("form-data.send") }}
                </v-btn>
              </v-col>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <v-dialog v-model="isReversal" max-width="500px">
          <v-card>
            <v-card-title>
              <span class="headline">{{ $t(`form-data.reversal`) }}</span>
            </v-card-title>

            <v-card-actions>
              <v-col class="text-center">
                <v-btn color="red darken-1" text @click="reversalTransaction">
                  {{ $t("form-data.reverseTransaction") }}
                </v-btn>
              </v-col>
            </v-card-actions>
          </v-card>
        </v-dialog>
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
import {
  getPaidList,
  getPaid,
  reversalTransaction,
  emailRecipt
} from '../../api'
import jsPDF from 'jspdf'
import moment from 'moment'
export default {
  name: 'paid',
  data: () => ({
    dialog: false,
    isPrint: false,
    isEmail: false,
    emailAddress: '',
    isReversal: false,
    editing: false,
    error: false,
    success: false,
    search: '',
    headers: [
      { text: 'Customer#', value: 'arrival.customer_id' },
      { text: 'Customer', value: 'arrival.customer' },
      { text: 'Payout#', value: 'arrival.id' },
      { text: 'Amount', value: 'arrival.price' },
      { text: 'Paid At', value: 'paid_at' },
      { text: 'User', value: 'username' }
    ],
    arrivalsHeader: [
      { text: 'Material', value: 'material.name' },
      { text: 'Net Kg', value: 'net_weight_kg' },
      { text: 'Price/kg', value: 'material.price_per_kg' },
      { text: 'Payout', value: 'payout' },
      { text: 'Arrival Time', value: 'arrived_at' },
      { text: 'Accepting User', value: 'username' }
    ],
    arrivals: [],
    fromDateMenu: false,
    items: [],
    editedIndex: -1,
    editedItem: {
      id: '',
      paid_at: '',
      paid_amount: 0,
      user: {
        id: '',
        email: '',
        firstname: '',
        lastname: '',
        status: ''
      },
      material: {
        name: ''
      },
      arrival: {
        id: '',
        customer: '',
        city: '',
        material: '',
        net_weight_kg: 0,
        arrived_at: '',
        price: 0,
        street: '',
        company_name: '',
        zip: ''
      }
    },
    token: ''
  }),

  watch: {
    dialog (val) {
      val || this.close()
    }
  },

  created () {
    this.initialize()
  },

  methods: {
    initialize () {
      this.token = document
        .querySelector('input[name="csrfmiddlewaretoken"]')
        .getAttribute('value')
      getPaidList(this.token)
        .then((res) => res.json())
        .then(({ result }) => {
          this.items = result.map((item) => ({
            id: item.id,
            paid_at: moment(item.paid_at).format('MM-DD-YYYY hh:mm'),
            // eslint-disable-next-line no-undef
            username: authUser.firstname + ' ' + authUser.lastname,
            arrival: {
              ...item.arrival,
              arrived_at: moment(item.arrival.arrived_at).format(
                'MM-DD-YYYY hh:mm'
              ),
              price: item.arrival.price.toFixed(2)
            }
          }))
        })
    },

    editItem (item) {
      this.editedIndex = this.items.indexOf(item)
      getPaid(item.id, this.token).then(({ result }) => {
        this.savedItem = Object.assign({}, result)
        this.arrivals = result.arrival.arrival_pos.map((item) => ({
          ...item,
          payout: (item.net_weight_kg * item.material.price_per_kg).toFixed(2),
          arrived_at: moment(result.arrived_at).format('MM-DD-YYYY hh:mm'),
          // eslint-disable-next-line no-undef
          username: authUser.firstname + ' ' + authUser.lastname
        }))
        this.dialog = true
        this.editing = true
      })
    },

    selectMaterial (material) {
      this.editedItem = {
        ...this.savedItem,
        ...material,
        paid_at: moment(this.savedItem.paid_at).format('MM-DD-YYYY hh:mm')
      }
    },

    close () {
      this.dialog = false
      this.editing = false
      this.$nextTick(() => {
        this.editedIndex = -1
      })
    },
    print () {
      this.isPrint = true
      const date = moment(new Date()).format('MM-DD-YYYY hh:mm')
      const pdfName = 'payout_transaction_' + date.replaceAll('-', '').trim()

      const addPages = (doc) => {
        const pageCount = doc.internal.getNumberOfPages()

        doc.setPage(1)
        // Header
        doc.setFont('helvetica', 'Bold')
        doc.setFontSize(20)
        doc.text(this.$t('pdf.customer'), 100, 70)
        doc.setFontSize(30)
        doc.text(
          this.$t('pdf.payout-title'),
          doc.internal.pageSize.width / 2,
          30,
          {
            align: 'center'
          }
        )
        doc.setFont('helvetica')
        doc.setFontSize(10)
        doc.text(
          `${this.$t('pdf.date')}: ` + date,
          doc.internal.pageSize.width - 10,
          30,
          {
            align: 'right'
          }
        )
        doc.setDrawColor('gray')
        doc.setLineWidth(0, 5)
        doc.line(10, 35, doc.internal.pageSize.width - 10, 35)

        doc.setFont('helvetica')
        doc.setFontSize(10)
        doc.text(this.$t('pdf.material'), 10, 50)
        doc.text(this.$t('pdf.arrival'), 10, 70)
        doc.text(this.$t('pdf.weight'), 10, 90)
        doc.text(this.$t('pdf.value'), 10, 110)
        doc.text(this.$t('pdf.paid-out'), 10, 130)
        doc.text(this.$t('pdf.paid-out-by'), 10, 150)
        doc.text(this.$t('table-data.name'), 100, 80)
        doc.text(this.$t('table-data.company'), 100, 100)
        doc.text(this.$t('table-data.address'), 100, 120)
        doc.text(
          this.$t('table-data.zip') + '/' + this.$t('table-data.city'),
          100,
          140
        )

        doc.setFont('helvetica', 'Bold')
        doc.setFontSize(15)
        doc.text(this.editedItem.material.name, 35, 50)
        doc.text(this.editedItem.arrived_at, 35, 70)
        doc.text(`${this.editedItem.net_weight_kg} kg`, 35, 90)
        doc.setFontSize(20)
        doc.text(this.editedItem.payout + 'EUR', 35, 110)
        doc.setFontSize(15)
        doc.text(this.editedItem.paid_at, 35, 130)
        doc.text(this.editedItem.username, 35, 150)

        doc.text(this.editedItem.arrival.customer, 120, 80)
        doc.text(this.editedItem.arrival.company_name, 120, 100)
        doc.text(this.editedItem.arrival.street, 120, 120)
        doc.text(
          `${this.editedItem.arrival.zip}/${this.editedItem.arrival.city}`,
          120,
          140
        )

        // Footer
        doc.setFont('helvetica', 'italic')
        doc.setFontSize(10)
        doc.text(
          'Page ' + String(1) + ' of ' + String(pageCount),
          doc.internal.pageSize.width / 2,
          287,
          {
            align: 'center'
          }
        )
      }
      const doc = new jsPDF()
      addPages(doc)
      doc.save(pdfName + '.pdf')
    },
    email () {
      this.isEmail = true
    },
    sendEmail () {
      if (this.emailAddress) {
        const data = {
          payout_id: this.editedItem.id,
          arrival_pos_id: this.editedItem.arrival.id,
          email: this.emailAddress
        }
        emailRecipt(data, this.token)
        this.isEmail = false
        this.emailAddress = ''
      }
    },
    reversal () {
      this.isReversal = true
    },
    reversalTransaction () {
      reversalTransaction(this.editedItem.id, this.token)
      this.items.splice(this.editedIndex, 1)
      this.isReversal = false
      this.close()
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.elevation-1 {
  margin-left: 260px;
}
.invite-error {
  color: white !important;
  padding-top: 10px !important;
}
</style>
