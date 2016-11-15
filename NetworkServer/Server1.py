from flask import Flask
from flask import request
from flask import jsonify, Response
import flask
import json
import ast
import sys
import random
from time import time
import hashlib
import gmpy
import copy

app = Flask(__name__)

def hash_int(x):
    return int(hashlib.md5(str(x)).hexdigest(),16)


@app.route('/getpk', methods=['GET'])
def getpk():
  #read server's public key
  fin=open("srv.pkey")
  n=fin.read()
  n=int(n.strip())
  return n


@app.route('/retrieveprofile', methods=['POST'])
def retrieveprofile():
  try:
    profile_number = request.form.get('profile')
    resp =  server_elements_cpy[int(profile_number)]
    return jsonify(resp=resp)
  except Exception as e:
      print e


@app.route('/', methods=['POST'])
def hello_world():

    vals = request.form.get('enc_data')

    try:
      print "Client values received"
      
      client_elements=json.loads(vals)
    
      print "Client values parsed"

      for index, profile in client_elements.iteritems():

        if (type(profile) is int 
            or type(profile) is unicode 
            or type(profile) is bool): 
       
            client_elements[index] = str(FastRSADecrypt(int(profile), dP, dQ, p, q, qInv))

        elif type(profile) is dict:            
            for key in profile:
              client_elements[index][key] = str(FastRSADecrypt(int(profile[key]), dP, dQ, p, q, qInv))
       
        elif type(profile) is list:
            for subindex, subitem in enumerate(profile):

              if type(subitem) is dict:
                for key in subitem:
                  client_elements[index][subindex][key] = str(FastRSADecrypt(int(subitem[key]), dP, dQ, p, q, qInv))
              elif type(subitem) is unicode:

                client_elements[index][subindex] = str(FastRSADecrypt(int(subitem), dP, dQ, p, q, qInv))

      print "Client elment checking done"
      m_B2 = []
      print "sending response..."
      resp = []
      resp.append(client_elements)
      resp = resp + server_elements
      return jsonify(resp=resp)

    except Exception as e:
      print e




e=2**16+1

#generates a random prime of the requested bit length
def gen_prime(BIT_LEN):
    found=False
    while found==False:
        p=random.randrange(2**(BIT_LEN-1),2**BIT_LEN)
        found=gmpy.is_prime(p)
    return p



def RSA_GEN(BIT_LEN):
    # this is faster but not so secure
    p=gen_prime(BIT_LEN)
    q=gen_prime(BIT_LEN)

    n=p*q
    f=(p-1)*(q-1)
    e=2**16+1
    d=gmpy.invert(e,f)
    return d,n

def RSA_ENC(m,n):
    return pow(m,e,n)
def RSA_DEC(c,d,n):

    return pow(c,d,n)


def FastRSADecrypt(c, dP, dQ, p, q, qInv):
   m1 = pow(c, dP, p)
   m2 = pow(c, dQ, q)
   h = (qInv * (m1 - m2)) % p
   return m2 + h * q

if __name__ == '__main__':


    p = int("7632433723502379096749125972149174910999884493717793629799267280562248320159478847529151476961445869529268745324239836669149274555600779122421297198762917")
    q = int("10010113632384840381817583618678712864701539929518796718949634240529828576446807320371955226242243642660169977522098589452748349618513577269884746782685379")
    d = int("5335761441782397234277447234913973201589175185447866954705307829918478026113498853291309468649025691088536692510101188431712139864088437299644669460473642261640495958458775315790900427648082799857147217568124167548444594999637191278982927661967296239864300239885211343388124155877797952742820716549114263881")
    n = int("76401528863904952489150329786881595305341877677233309287857059045087894777671045302196318253627091264336777194021084025835507649174735397707409373482862393194466338546059932547698937851434291422254193216437880662517954000639540828451495436650148843556671167988287429211842659543191848230350764449474023290543")

    dP = gmpy.invert(e, p - 1)
    dQ = gmpy.invert(e, q - 1)
    qInv = gmpy.invert(q, p)

    fname = "collective_elements.txt"
    with open(fname) as f:
      content = f.readlines()

    server_elements = []
    for srv_val in content:
      server_elements.append(json.loads(srv_val))

    server_elements_cpy = copy.deepcopy(server_elements)
    for index, profile in enumerate(server_elements): 
       for item in profile:          
          if (type(profile[item]) is int 
            or type(profile[item]) is unicode):

            profile[item] = hash_int(profile[item])
            profile[item] = str(hash_int(FastRSADecrypt(profile[item], dP, dQ, p, q, qInv)))
          elif type(profile[item]) is bool:
            profile[item] = str(profile[item]).lower()

            profile[item] = hash_int(profile[item])
            profile[item] = str(hash_int(FastRSADecrypt(profile[item], dP, dQ, p, q, qInv)))
          
          elif type(profile[item]) is dict:
          
            for key in profile[item]:
              if type(profile[item][key]) is bool:
                profile[item][key] = str(profile[item][key]).lower()

          
              profile[item][key] = hash_int(profile[item][key])
              profile[item][key] = str(hash_int(FastRSADecrypt(profile[item][key], dP, dQ, p, q, qInv)))
          
          elif type(profile[item]) is list:
            for subindex, subitem in enumerate(profile[item]):

              if type(subitem) is dict:
                for key in subitem:
                  if type(subitem[key]) is bool:
                    subitem[key] = str(subitem[key]).lower()

                    
                  subitem[key] = hash_int(subitem[key])
                  subitem[key] = str(hash_int(FastRSADecrypt(subitem[key], dP, dQ, p, q, qInv)))
              elif type(subitem) is unicode:

                profile[item][subindex] = hash_int(subitem)
                profile[item][subindex] = str(hash_int(FastRSADecrypt(profile[item][subindex], dP, dQ, p, q, qInv)))

    app.run(port=3001, host='0.0.0.0', threaded=True) 