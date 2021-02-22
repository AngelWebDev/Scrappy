<template>
  <v-data-table
    :headers="headers"
    :items="items"
    class="elevation-1"
    @click:row="editItem"
  >
    <template v-slot:top>
      <v-toolbar flat>
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
                      v-model="editedItem.datetime"
                      :label="$t('table-data.paid_out_at')"
                    />
                    <v-text-field
                      outlined
                      v-model="editedItem.amount"
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
                          {{ editedItem.name }}
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
                          n/a
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
                          {{ editedItem.address }}
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

    <template v-slot:no-data>
      <v-btn color="primary" @click="initialize">
        Reset
      </v-btn>
    </template>
  </v-data-table>
</template>

<script>
import { getUsers } from "../../api";
import moment from "moment";
export default {
  name: "open",
  data: () => ({
    dialog: false,
    editing: false,
    error: false,
    success: false,
    headers: [
      { text: "Customer", value: "name" },
      { text: "City", value: "city" },
      { text: "Material", value: "material" },
      { text: "Weight", value: "weight" },
      { text: "Date/Time", value: "date" },
      { text: "Amount", value: "amount" },
    ],
    fromDateMenu: false,
    items: [],
    editedIndex: -1,
    editedItem: {
      id: "",
      firstname: "",
      lastname: "",
      email: "",
      datetime: "",
      payout: false,
      office: false,
    },
    defaultItem: {
      id: "",
      firstname: "",
      lastname: "",
      email: "",
      arrival: false,
      payout: false,
      office: false,
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
      getUsers(this.token)
        .then((res) => res.json())
        .then(({ result }) => {
          this.items = result.map((item) => ({
            name: item.firstname + " " + item.lastname,
            ...item,
          }));
        });
    },

    editItem(item) {
      this.editedIndex = this.items.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
      this.editing = true;
      this.editedItem.datetime = moment(new Date()).format("MM-DD-YYYY hh:mm");
    },

    paid() {},

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
