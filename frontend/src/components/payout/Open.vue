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
              <v-spacer></v-spacer>
              <v-btn color="red darken-1" text @click="close">
                {{ $t("form-data.cancel") }}
              </v-btn>
              <v-btn color="blue darken-1" text @click="paid">
                {{ $t("payout.paid") }}
              </v-btn>
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
import { getOpenList, getOpen, createPaid } from "../../api";
import moment from "moment";
export default {
  name: "open",
  data: () => ({
    dialog: false,
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
