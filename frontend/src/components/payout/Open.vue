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
        <v-dialog v-model="dialog" max-width="700px">
          <v-card>
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
                    <v-text-field
                      outlined
                      disabled
                      v-model="editedItem.arrived_at"
                      :label="$t('table-data.paid_out_at')"
                    />
                    <v-text-field
                      outlined
                      v-model="editedItem.price"
                      :label="$t('table-data.amount')"
                      suffix="EUR"
                    />
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-row class="text-left pa-2 ma-0">
                      <v-col class="text-left pa-0 ma-0">
                        <span class="doc_title">
                          {{ $t("table-data.name") }} :
                        </span>
                      </v-col>
                      <v-col class="text-left pa-0 ma-0">
                        <strong>
                          {{ editedItem.customer }}
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
                          {{ editedItem.company_name }}
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
                          {{ editedItem.street }}
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
                          {{ editedItem.zip }}/{{ editedItem.city }}
                        </strong>
                      </v-col>
                    </v-row>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-select
                dense
                :items="ids"
                v-model="selectedId"
                v-on:change="selectId"
                outlined
                class="pt-6 pr-2"
              />
              <v-btn
                color="warning"
                dark
                @click="verifyCustomer"
                v-if="editedItem.identification"
              >
                {{ $t("table-data.verify_customer") }}
              </v-btn>
              <v-btn color="grey darken-1" text @click="changeCustomer">
                {{ $t("form-data.change-customer") }}
              </v-btn>
              <v-btn color="red darken-1" text @click="close">
                {{ $t("form-data.cancel") }}
              </v-btn>
              <v-btn color="blue darken-1" text @click="paid">
                {{ $t("payout.paid") }}
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <v-dialog v-model="dialogID" max-width="600px">
          <v-card height="750px">
            <v-card-title>
              <span class="headline">{{ $t(`form-data.id_person`) }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12" sm="12">
                    <p class="text-left pa-0 ma-0">
                      {{ editedItem.customer }}
                    </p>
                    <p class="text-left pa-0 ma-0">
                      {{ editedItem.street }}
                    </p>
                    <p class="text-left ma-0">
                      {{ editedItem.zip + " " + editedItem.city }}
                    </p>
                    <p class="text-left mt-0 mb-8">
                      {{ editedItem.company_name }}
                    </p>
                    <v-row>
                      <v-col cols="12" class="py-0">
                        <v-select
                          outlined
                          :items="types"
                          :label="$t('table-data.doc_type')"
                          v-model="identification.document_type"
                        ></v-select>
                      </v-col>
                    </v-row>
                    <v-row>
                      <v-col cols="12" class="py-0">
                        <v-text-field
                          outlined
                          v-model="identification.document_id_number"
                          :label="$t('table-data.doc_number')"
                        ></v-text-field>
                      </v-col>
                    </v-row>
                    <v-row>
                      <v-col cols="12" class="py-0">
                        <v-text-field
                          outlined
                          v-model="identification.issuing_country"
                          :label="$t('table-data.doc_issuer')"
                        ></v-text-field>
                      </v-col>
                    </v-row>
                    <v-row>
                      <v-col cols="12" class="py-0">
                        <v-text-field
                          outlined
                          v-model="identification.name_on_document"
                          :label="$t('table-data.doc_name')"
                        ></v-text-field>
                      </v-col>
                    </v-row>
                    <v-row>
                      <v-col cols="12" class="py-0">
                        <v-menu
                          v-model="fromDateMenu"
                          :close-on-content-click="false"
                          :nudge-right="40"
                          lazy
                          transition="scale-transition"
                          offset-y
                          full-width
                          max-width="290px"
                          min-width="290px"
                        >
                          <template v-slot:activator="{ on }">
                            <v-text-field
                              outlined
                              :label="$t('table-data.doc_exp')"
                              readonly
                              :value="identification.document_expiration_date"
                              v-on="on"
                            ></v-text-field>
                          </template>
                          <v-date-picker
                            locale="en-in"
                            v-model="identification.document_expiration_date"
                            no-title
                            @input="fromDateMenu = false"
                          ></v-date-picker>
                        </v-menu>
                      </v-col>
                    </v-row>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-container>
                <v-row>
                  <v-col cols="6">
                    <v-btn color="grey darken-1" text @click="cancelDoc">
                      {{ $t("form-data.cancel") }}
                    </v-btn>
                  </v-col>

                  <v-col cols="6">
                    <v-btn color="blue darken-1" text @click="saveDoc">
                      {{ $t("form-data.save") }}
                    </v-btn>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <v-dialog v-model="isChangeCustomer" max-width="600px">
          <v-card height="250px">
            <v-card-title>
              <span class="headline">{{ $t(`form-data.id_person`) }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12" sm="12">
                    <v-autocomplete
                      v-model="customer_id"
                      :items="customers"
                      outlined
                      dense
                      chips
                      small-chips
                      :label="$t('table-data.customer')"
                      v-on:change="onChange"
                    />
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-container>
                <v-row>
                  <v-col cols="6">
                    <v-btn
                      color="grey darken-1"
                      text
                      @click="cancelChangeCustomer"
                    >
                      {{ $t("form-data.cancel") }}
                    </v-btn>
                  </v-col>

                  <v-col cols="6">
                    <v-btn color="blue darken-1" text @click="selectCustomer">
                      {{ $t("form-data.select") }}
                    </v-btn>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>

    <template v-slot:[`item.price`]="{ item }"> {{ item.price }} EUR </template>

    <template v-slot:no-data>
      <v-btn color="primary" @click="initialize">
        Reset
      </v-btn>
    </template>
  </v-data-table>
</template>

<script>
import {
  getOpenList,
  getOpen,
  createPaid,
  verifyIdentification,
  getCustomers,
  getCustomer,
  changeCustomer,
} from "../../api";
import moment from "moment";
export default {
  name: "open",
  data: () => ({
    dialog: false,
    dialogID: false,
    isChangeCustomer: false,
    editing: false,
    error: false,
    success: false,
    search: "",
    headers: [
      { text: "Customer#", value: "customer_id" },
      { text: "Customer", value: "customer" },
      { text: "City", value: "city" },
      { text: "Date/Time", value: "arrived_at" },
      { text: "Amount", value: "price" },
    ],
    fromDateMenu: false,
    items: [],
    types: [
      { value: "passport", text: "Passport" },
      { value: "idcard", text: "ID Card" },
      { value: "driverlicense", text: "Driver License" },
    ],
    identification: {
      document_type: "passport",
      document_id_number: "",
      name_on_document: null,
      issuing_country: null,
      document_expiration_date: null,
    },
    defaultIdentification: {
      document_type: "passport",
      document_id_number: "",
      name_on_document: null,
      issuing_country: null,
      document_expiration_date: null,
    },
    editedIndex: -1,
    editedItem: {
      id: "",
      arrived_at: "",
      city: "",
      customer: "",
      material: "",
      net_weight_kg: 0,
      price: 0,
      street: "",
      zip: "",
      company_name: "",
    },
    defaultItem: {
      id: "",
      arrived_at: "",
      city: "",
      customer: "",
      material: "",
      net_weight_kg: 0,
      price: 0,
      street: "",
      zip: "",
      company_name: "",
    },
    ids: [],
    selectedId: "",
    customers: [],
    customer_id: "",
    token: "",
  }),

  watch: {
    dialog(val) {
      val || this.close();
    },
    dialogDelete(val) {
      val || this.closeDelete();
    },
  },

  created() {
    this.initialize();
  },

  methods: {
    initialize() {
      this.token = document
        .querySelector('input[name="csrfmiddlewaretoken"]')
        .getAttribute("value");
      getOpenList(this.token)
        .then((res) => res.json())
        .then(({ result }) => {
          this.items = result.map((item) => ({
            ...item,
            arrived_at: moment(item.arrived_at).format("MM-DD-YYYY hh:mm"),
          }));
        });
    },

    openDialogID() {
      this.dialogID = true;
    },

    selectId() {
      if (this.selectedId === -1) {
        this.openDialogID();
      }
    },

    verifyCustomer() {
      //console.log("angel log", this.editedItem.id, this.selectedId);
      //call api
    },

    cancelDoc() {
      this.dialogID = false;
      this.identification = Object.assign({}, this.defaultIdentification);
    },

    saveDoc() {
      this.identification.verified_at = moment(new Date()).format(
        "MM-DD-YYYY hh:mm"
      );
      Object.assign(this.items[this.editedIndex], this.editedItem);
      const data = {
        customer_id: this.editedItem.customer_id,
        document_type: this.identification.document_type,
        document_id_number: this.identification.document_id_number,
        name_on_document: this.identification.name_on_document,
        issuing_country: this.identification.issuing_country,
        document_expiration_date: this.identification.document_expiration_date,
      };
      verifyIdentification(data, this.token).then(() => {
        getCustomer(this.editedItem.customer_id, this.token).then((res) => {
          if (res.result.identification.length > 0) {
            const resultIds = res.result.identification.map((item) => ({
              text: item.document_type,
              value: item.id,
            }));

            this.ids = [...resultIds, { text: "Enter New Doc", value: -1 }];
          }
        });
      });
      this.dialogID = false;
    },

    editItem(item) {
      getOpen(item.id, this.token).then(({ result }) => {
        this.editedIndex = this.items.indexOf(item);
        if (result) {
          this.editedItem = Object.assign({}, result);
        }
        this.dialog = true;
        this.editing = true;
        this.editedItem.arrived_at = moment(new Date()).format(
          "MM-DD-YYYY hh:mm"
        );
      });
      getCustomer(item.customer_id, this.token).then((res) => {
        if (res.result.identification.length > 0) {
          const resultIds = res.result.identification.map((item) => ({
            text: item.document_type,
            value: item.id,
          }));

          this.ids = [...resultIds, { text: "Enter New Doc", value: -1 }];
        }
      });
    },

    paid() {
      createPaid(this.editedItem.id, this.token).then(({ result }) => {
        if (result === "success") {
          this.initialize();
          this.close();
        }
      });
    },

    close() {
      this.dialog = false;
      this.editing = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    closeDelete() {
      this.dialogDelete = false;
      this.editedItem = Object.assign({}, this.defaultItem);
      this.editedIndex = -1;
    },

    changeCustomer() {
      this.isChangeCustomer = true;
      getCustomers(this.token)
        .then((res) => res.json())
        .then(({ result }) => {
          this.customers = result.map((item) => ({
            value: item.id,
            text: item.company
              ? item.firstname +
                " " +
                item.lastname +
                ", " +
                item.company.name +
                ", " +
                item.street +
                ", " +
                item.zip
              : item.firstname +
                " " +
                item.lastname +
                ", " +
                item.street +
                ", " +
                item.zip,
          }));
        });
    },

    onChange(id) {
      this.error = "";
      this.customer_id = id;
    },

    cancelChangeCustomer() {
      this.isChangeCustomer = false;
      this.customer_id = "";
    },
    selectCustomer() {
      changeCustomer(this.editedItem.id, this.customer_id, this.token).then(
        () => {
          this.cancelChangeCustomer();
          this.close();
          this.initialize();
        }
      );
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
