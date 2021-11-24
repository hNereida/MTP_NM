FIXED_PART = {
    "fields": {
        "source_address": {
            "static": True,
            "byte_start": 0,
            "bit_start": 0,
            "byte_end": 0,
            "bit_end": 2
        },
        "destination_address": {
            "static": True,
            "byte_start": 0,
            "bit_start": 3,
            "byte_end": 0,
            "bit_end": 5
        }, 
        "type": {
            "static": True,
            "byte_start": 0,
            "bit_start": 6,
            "byte_end": 1,
            "bit_end": 0
        }
    }
}

HELLO = {
  "type": 0,
  "fields": {}
}

HELLO_RESPONSE = {
  "type": 1,
  "fields": {
    "have_data": {
      "static": True,
      "byte_start": 1,
      "bit_start": 1,
      "byte_end": 1,
      "bit_end": 1
    },
    "have_token": {
      "static": True,
      "byte_start": 1,
      "bit_start": 2,
      "byte_end": 1,
      "bit_end": 2
    }
  }
}

DATA = {
  "type": 2,
  "fields": {
    "length": {
      "static": True,
      "byte_start": 1,
      "bit_start": 1,
      "byte_end": 1,
      "bit_end": 5
    }, 
    "eot": {
      "static": True,
      "byte_start": 1,
      "bit_start": 6,
      "byte_end": 1,
      "bit_end": 6
    }, 
    "sequence_number": {
      "static": True,
      "byte_start": 1,
      "bit_start": 7,
      "byte_end": 1,
      "bit_end": 7
    },
    "payload": {
      "static": False,
      "byte_start": 2,
      "bit_start": 0
    }, 
  }
}

DATA_RESPONSE = {
  "type": 3,
  "fields": {
    "sequence_number": {
      "static": True,
      "byte_start": 1,
      "bit_start": 1,
      "byte_end": 1,
      "bit_end": 1
    },
    "ack_nack": {
      "static": True,
      "byte_start": 1,
      "bit_start": 2,
      "byte_end": 1,
      "bit_end": 2
    }
  }
}

TOKEN = {
  "type": 2,
  "fields": {
    "num_recv_data": {
      "static": True,
      "byte_start": 1,
      "bit_start": 1,
      "byte_end": 1,
      "bit_end": 3
    }
  }
}

TOKEN_RESPONSE = {
  "type": 3,
  "fields": {
    "ack_nack": {
      "static": True,
      "byte_start": 1,
      "bit_start": 1,
      "byte_end": 1,
      "bit_end": 1
    }
  }
}