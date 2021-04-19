<template v-slot:extension>
  <v-container fluid class="arrival_container col-8">
    <h1 class="tab-title text-left pb-16">{{ $t("side-bar.arrival") }}</h1>
    <v-row>
      <v-col cols="7">
        <v-autocomplete
          v-model="form.customer_id"
          :items="customers"
          outlined
          dense
          chips
          small-chips
          :label="$t('table-data.customer')"
          v-on:change="onChange"
        />
        <v-select
          dense
          :items="materials"
          v-model="form.material_id"
          :label="$t('table-data.material')"
          outlined
        />

        <v-row>
          <v-col cols="4">
            <v-text-field
              dense
              :label="$t('table-data.weight')"
              v-model="form.gross_weight_kg"
              outlined
              type="number"
              suffix="kg"
            />
          </v-col>
          <v-col cols="4">
            <v-text-field
              dense
              :label="$t('table-data.tare')"
              v-model="form.tare_kg"
              outlined
              type="number"
              suffix="kg"
            />
          </v-col>
          <v-col cols="4">
            <v-text-field
              dense
              :label="$t('table-data.net')"
              :value="form.gross_weight_kg - form.tare_kg"
              outlined
              disabled
              type="number"
              suffix="kg"
            />
          </v-col>
        </v-row>
      </v-col>
      <v-col cols="5" class="text-left pr-12">
        <v-simple-table v-if="customer.id !== null">
          <template v-slot:default>
            <tbody>
              <tr>
                <td>{{ $t("table-data.name") }}:</td>
                <td>{{ customer.firstname + " " + customer.lastname }}</td>
              </tr>
              <tr>
                <td>{{ $t("table-data.company") }}:</td>
                <td>{{ customer.company.name }}</td>
              </tr>
              <tr>
                <td>{{ $t("table-data.address") }}:</td>
                <td>{{ customer.street }}</td>
              </tr>
              <tr>
                <td>
                  {{ $t("table-data.zip") }} / {{ $t("table-data.city") }}:
                </td>
                <td>{{ customer.zip + "/" + customer.city }}</td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6">
        <v-btn depressed @click="cancel">
          {{ $t("form-data.clear") }}
        </v-btn>
      </v-col>
      <v-col cols="3">
        <v-btn depressed color="primary" @click="save">
          {{ $t("form-data.save") }}
        </v-btn>
      </v-col>
      <v-col cols="3">
        <v-btn depressed color="primary" @click="finish">
          {{ $t("form-data.finish") }}
        </v-btn>
      </v-col>
    </v-row>
    <br />
    <br />
    <div class="text-center" v-if="error">
      <span class="red--text">{{ error }} </span>
    </div>
    <v-data-table
      :headers="headers"
      :items="items"
      :hide-default-footer="true"
      class="elevation-1"
      v-if="items.length > 0"
    >
      <template v-slot:[`item.actions`]="{ item }">
        <v-icon small @click="deleteItem(item)">
          mdi-delete
        </v-icon>
      </template>
    </v-data-table>
  </v-container>
</template>

<script>
import {
  getCustomers,
  getCustomer,
  createArrival,
  getMaterials,
  getArrivalPosList,
  deleteArrivalPos,
} from "../api";
export default {
  name: "arrival",
  data() {
    return {
      headers: [
        { text: "Material", value: "material.name" },
        { text: "Gross Kg", value: "gross_weight_kg" },
        { text: "Tare Kg", value: "tare_kg" },
        { text: "Net Kg", value: "net_weight_kg" },
        { text: "Actions", value: "actions" },
      ],
      customers: [],
      items: [],
      customer: {
        id: null,
        firstname: "",
        lastname: "",
        street: null,
        zip: null,
        city: null,
        company: {
          id: "",
          name: "",
          tax_id: "",
          vat_id: "",
        },
      },
      materials: [],
      form: {
        customer_id: null,
        material_id: null,
        gross_weight_kg: 0,
        tare_kg: 0,
      },
      error: "",
      token: "",
    };
  },
  created() {
    this.token = document
      .querySelector('input[name="csrfmiddlewaretoken"]')
      .getAttribute("value");
    this.initialize();
  },
  methods: {
    initialize() {
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

      getMaterials(this.token)
        .then((res) => res.json())
        .then(({ result }) => {
          this.materials = result.map((item) => ({
            value: item.id,
            text: item.name,
          }));
        });
    },
    onChange(id) {
      this.error = "";
      getCustomer(id, this.token).then((res) => {
        if (res) {
          if (!res.result.company) {
            res.result.company = Object.assign(
              {},
              {
                id: "",
                name: "",
                tax_id: "",
                vat_id: "",
              }
            );
          }
          this.customer = Object.assign({}, res.result);
        }
      });
      getArrivalPosList(this.form.customer_id, this.token)
        .then((res) => res.json())
        .then(({ result }) => {
          this.items = result.length ? result : [{}];
        })
        .catch(() => (this.items = []));
    },
    save() {
      this.validation();

      if (this.error !== "") return;

      const payload = {
        ...this.form,
        arrived_at: new Date(),
      };

      createArrival(payload, this.token).then((res) => {
        if (res.status === 200) {
          this.form.material_id = null;
          this.form.gross_weight_kg = 0;
          this.form.tare_kg = 0;
          getArrivalPosList(this.form.customer_id, this.token)
            .then((res) => res.json())
            .then(({ result }) => {
              this.items = result;
            });
        } else {
          this.error = "Something went wrong";
        }
      });
    },
    finish() {
      this.validation();

      if (this.error !== "") return;

      createArrival(this.form, this.token).then((res) => {
        if (res.status === 200) {
          this.cancel();
        } else {
          this.error = "Something went wrong";
        }
      });
    },
    deleteItem(item) {
      deleteArrivalPos(item.id, this.token).then(() => {
        getArrivalPosList(this.form.customer_id, this.token)
          .then((res) => res.json())
          .then(({ result }) => {
            this.items = result;
          });
      });
    },
    validation() {
      if (this.form.customer_id === null) {
        this.error = "Please select a customer";
      } else if (this.form.material_id === null) {
        this.error = "Please select a Material";
      } else if (this.form.gross_weight_kg === 0) {
        this.error = "Gross Weight can not be 0";
      } else if (
        Number(this.form.tare_kg) >= Number(this.form.gross_weight_kg)
      ) {
        this.error = "Gross Weight must be greater than Tare Weight";
      } else {
        this.error = "";
      }
    },
    cancel() {
      this.customer = Object.assign(
        {},
        {
          id: null,
          firstname: "",
          lastname: "",
          street: null,
          zip: null,
          city: null,
          company: {
            id: "",
            name: "",
            tax_id: "",
            vat_id: "",
          },
        }
      );
      this.error = "";
      this.form = Object.assign(
        {},
        {
          customer_id: null,
          material_id: null,
          gross_weight_kg: 0,
          tare_kg: 0,
        }
      );
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.arrival_container {
  width: calc(100% - 260px);
  margin-top: 140px;
  margin-left: 260px;
  padding: 30px;
}
</style>
