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
                    <v-row class="text-left pa-2 ma-0">
                      <v-col class="text-left pa-0 ma-0">
                        <span class="doc_title">
                          {{ $t("table-data.material") }} :
                        </span>
                      </v-col>
                      <v-col class="text-left pa-0 ma-0">
                        <strong>
                          {{ editedItem.arrival.material }}
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
                          {{ editedItem.arrival.arrived_at }}
                        </strong>
                      </v-col>
                    </v-row>

                    <v-row class="text-left pa-2 ma-0">
                      <v-col class="text-left pa-0 ma-0">
                        <span class="doc_title">
                          {{ $t("table-data.weight") }} :
                        </span>
                      </v-col>
                      <v-col class="text-left pa-0 ma-0">
                        <strong>
                          {{ editedItem.arrival.net_weight_kg }} kg
                        </strong>
                      </v-col>
                    </v-row>

                    <v-row class="text-left pa-2 ma-0">
                      <v-col class="text-left pa-0 ma-0">
                        <span class="doc_title">
                          {{ $t("table-data.value") }} :
                        </span>
                      </v-col>
                      <v-col class="text-left pa-0 ma-0">
                        <h2>{{ editedItem.arrival.price }} EUR</h2>
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
                          {{
                            editedItem.user.firstname +
                              " " +
                              editedItem.user.lastname
                          }}
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

            <!-- <v-card-text>
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
            </v-card-text> -->

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
import { getPaidList, getPaid } from "../../api";
import moment from "moment";
export default {
  name: "paid",
  data: () => ({
    dialog: false,
    isPrint: false,
    isEmail: false,
    emailAddress: "",
    isReversal: false,
    editing: false,
    error: false,
    success: false,
    search: "",
    headers: [
      { text: "Customer#", value: "arrival.customer_id" },
      { text: "Customer", value: "arrival.customer" },
      { text: "Payout#", value: "arrival.id" },
      { text: "Amount", value: "arrival.price" },
      { text: "Paid At", value: "paid_at" },
      { text: "User", value: "username" },
    ],
    fromDateMenu: false,
    items: [],
    editedIndex: -1,
    editedItem: {
      id: "",
      paid_at: "",
      paid_amount: 0,
      user: {
        id: "",
        email: "",
        firstname: "",
        lastname: "",
        status: "",
      },
      arrival: {
        id: "",
        customer: "",
        city: "",
        material: "",
        net_weight_kg: 0,
        arrived_at: "",
        price: 0,
        street: "",
        company_name: "",
        zip: "",
      },
    },
    token: "",
  }),

  watch: {
    dialog(val) {
      val || this.close();
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
      getPaidList(this.token)
        .then((res) => res.json())
        .then(({ result }) => {
          this.items = result.map((item) => ({
            id: item.id,
            paid_at: moment(item.paid_at).format("MM-DD-YYYY hh:mm"),
            // eslint-disable-next-line no-undef
            username: authUser.firstname + " " + authUser.lastname,
            arrival: {
              ...item.arrival,
              arrived_at: moment(item.arrival.arrived_at).format(
                "MM-DD-YYYY hh:mm"
              ),
            },
          }));
        });
    },

    editItem(item) {
      this.editedIndex = this.items.indexOf(item);
      getPaid(item.id, this.token).then(({ result }) => {
        this.editedItem = Object.assign({}, result);
        this.editedItem.paid_at = moment(this.editedItem.paid_at).format(
          "MM-DD-YYYY hh:mm"
        );
        this.editedItem.arrival.arrived_at = moment(
          this.editedItem.arrival.arrived_at
        ).format("MM-DD-YYYY hh:mm");
        this.dialog = true;
        this.editing = true;
      });
    },

    close() {
      this.dialog = false;
      this.editing = false;
      this.$nextTick(() => {
        this.editedIndex = -1;
      });
    },
    print() {
      this.isPrint = true;
    },
    email() {
      this.isEmail = true;
    },
    sendEmail() {
      if (this.emailAddress) {
        //call api
        this.isEmail = false;
        this.emailAddress = "";
      }
    },
    reversal() {
      this.isReversal = true;
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
